
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from .HelperFunction import *
from django.contrib.auth import logout
from .forms import *



def getlist(file_path):
    import pandas as pd
    LIST_CONTACTS= []
    valid = True
    csv_file = open(file_path)
    df = pd.read_csv(csv_file)
    try:
        saved_column = df['phone']
    except KeyError:
        try:
            saved_column = df['contacts']
        except KeyError:
            try:
                saved_column = df['contact']
            except KeyError:
                try:
                    saved_column =df['numbers']
                except KeyError:
                    try:
                        saved_column = df['number']
                    except KeyError:
                        print('Error CSV')
                        valid = False
    if valid:
        for contact in saved_column:
            contact = str(contact)
            contact.replace('-','')
            contact.replace('+','')
            contact.replace('.0','')
            if len(contact)<10:
                contact='9417290392'
            if len(contact)==10:
                contact = '91'+contact
            elif len(contact) > 10:
                contact = contact[-10:]
                contact = '91'+ contact
            LIST_CONTACTS.append(contact)

    return LIST_CONTACTS


def hasAdmin(user):
    adminObj = Admin.objects.get(authUser = user)
    if not adminObj:
        return False
    else:
        return True

# Create your views here.
def login(request):
    dictv={}

    if request.user.is_authenticated() :
        return HttpResponseRedirect('/dashboard/')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= auth.authenticate(username= username, password= password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/dashboard/')
        else:
            dictv['error']="Invalid Credentials"

    return render(request,'login.html',dictv)

@login_required
@user_passes_test(hasAdmin)
def dashboard(request):
    dictv={}
    obj_Admin = get_object_or_404(Admin,authUser = request.user)
    obj_AdminBot = AdminBot.objects.filter( admin_id = obj_Admin ).order_by('-pk')
    dictv['AdminBots']= obj_AdminBot
    return render(request,'dashboard_home.html',dictv)

@login_required
@user_passes_test(hasAdmin)
def registerbot(request):
    dictv = {}
    if request.method == 'POST':
        admin = Admin.objects.get(authUser = request.user)
        ph = request.POST.get('ph')
        cc = request.POST.get('cc')
        otp = request.POST.get('otp')

        ph = str(cc)+str(ph)
        dictv = registercode(ph,cc,otp)
        print(dictv)
        if dictv.get('status') == "'ok'":
            # Create Bot and AdminBot instances
            bot = Bot.objects.create(bot_phone = ph,bot_otp = otp,bot_pwd = dictv['pw'][1:-1])
            adminBot = AdminBot.objects.create(admin_id = admin,bot_id = bot)

    return render(request,'registerBot.html',dictv)


@login_required
@user_passes_test(hasAdmin)
def sendOtp(request):
    dictv = {}
    phoneNumber = request.GET.get('ph')
    countryCode = request.GET.get('cc')
    print('Got Phone number ')
    print(phoneNumber , countryCode )
    dictv = getcode(phoneNumber,countryCode,'voice')
    print(dictv)
    return JsonResponse(dictv)



@login_required
@user_passes_test(hasAdmin)
def  messages(request):
    dictv = {}
    obj_Admin = get_object_or_404(Admin,authUser = request.user)
    obj_messages = Message.objects.filter( admin = obj_Admin ).order_by('-pk')
    dictv['Messages'] = obj_messages
    return render(request,'messages.html',dictv)




# Using Get request to get Message Id;

# and thus Corresponding Details
@login_required
@user_passes_test(hasAdmin)
def messageDetails(request,pk):
    dictv = {}
    messageID= pk
    print("messageID: " ,messageID)
    obj_Admin = get_object_or_404(Admin,authUser = request.user)
    obj_message = Message.objects.get( admin = obj_Admin , id =messageID )
    obj_details = MessageStatus.objects.filter(message_id =obj_message )
    dictv['Details'] = obj_details
    dictv['content'] = obj_message
    return render(request,'message_details.html',dictv)





@login_required
@user_passes_test(hasAdmin)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')






@login_required
@user_passes_test(hasAdmin)
def mediafetch(request):
    return HttpResponseRedirect(request.get_full_path())



@login_required
@user_passes_test(hasAdmin)
def suspend(request):
    if request.method == 'POST':
        admin = Admin.objects.get(authUser = request.user)
        botId=request.POST.get('bot_id')
        messageId=request.POST.get('message_id')



@login_required
@user_passes_test(hasAdmin)
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            document_obj = Document.objects.filter( id = newdoc.id ).order_by('-pk')

            # Redirect to the document list after POST
            return render(request,'upload_csv.html',{'document_id': document_obj, 'form': form})

            # return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'upload_csv.html',
        {'documents': documents, 'form': form}
        )

@login_required
@user_passes_test(hasAdmin)
def compose_message(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        admin_obj = Admin.objects.get(authUser = request.user)
        message_content = request.POST.get('message_content')
        bot_obj = Bot.objects.all()
        bot_count = bot_obj.count()
        bot_obj = bot_obj[0]

        if not (bot_count):
            render(request,'compose_message.html',{'message':1})
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            document_obj = Document.objects.filter( id = newdoc.id ).order_by('-pk')
            message_object = Message.objects.create(message_text=message_content ,csvFile= newdoc.docfile.path , admin= admin_obj)
            LIST_CONTACTS =  getlist(newdoc.docfile.path)
            if not LIST_CONTACTS:
                render(request,'compose_message.html',{'message':2})
            for contact in LIST_CONTACTS:
                message_status_model = MessageStatus.objects.create(message_id = message_object , phon_num = contact , bot_id = bot_obj )


            # Redirect to the composeMessage with success after POST
            return render(request,'compose_message.html',{'message': 0, 'form': form})

    return render(request,'compose_message.html' ,{'form':form})

@login_required
@user_passes_test(hasAdmin)
def send_sms(request):
    dictv= {}
    list_id = request.POST.get('listId')
    message_content = request.POST.get('message_content')
    #insert into database
    return JsonResponse(dictv)
