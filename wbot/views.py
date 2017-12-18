
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
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            document_obj = Document.objects.filter( id = newdoc.id ).order_by('-pk')
            # Redirect to the document list after POST
            dictv['document_id'] = document_obj
            dictv['form'] = form

            return render(request,'dashboard_home.html',dictv)
            # return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    dictv['documents']=documents

    dictv['form'] = form

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
    obj_details = MessageStatus.objects.filter(message_id =messageID )
    dictv['Details'] = obj_details
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
