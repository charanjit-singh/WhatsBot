from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from .HelperFunction import *
from django.contrib.auth import logout






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
        print(cc)
        print(ph)
        ph = str(cc)+str(ph)
        print(ph)
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
    dictv = getcode(phoneNumber,countryCode,'sms')
    return JsonResponse(dictv)



@login_required
@user_passes_test(hasAdmin)
def  messages(request):
    dictv = {}

    obj_Admin = get_object_or_404(Admin,authUser = request.user)
    obj_messages = Message.objects.filter( admin = obj_Admin ).order_by('-pk')
    dictv['Messages'] = obj_messages
    return render(request,'messages.html',dictv)




# Using Get request to get Message Id
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
