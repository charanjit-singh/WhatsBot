from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import *
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

def dashboard(request):
    dictv={}
    obj_Admin = get_object_or_404(Admin,authUser = request.user)
    obj_AdminBot = AdminBot.objects.filter( admin_id = obj_Admin ).order_by('-pk')
    dictv['AdminBots']= obj_AdminBot

    return render(request,'dashboard_home.html',dictv)
