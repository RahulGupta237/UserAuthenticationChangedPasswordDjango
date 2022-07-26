
from email import message
from django.shortcuts import render,HttpResponseRedirect

from .forms import SignUpForm

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def user_signup(request):

    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            print("data successfullya saved")
            messages.success(request,"Congratullation your account successfully created")
            return HttpResponseRedirect('login')

    else:

        fm=SignUpForm()
        print("get the form data")

    return render(request,'UserApp/signup.html',{"forms":fm})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    
    else:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    print("i am login rahul")
                    messages.success(request,"successfully login")
                    return HttpResponseRedirect('/profile/')
                else:
                    print("you are fake")
                    messages.error(request,f"wrong credential for {uname}")
        else:
            fm=AuthenticationForm()
        return render(request,"UserApp/login.html",{"forms":fm})

def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'UserApp/Home.html',{"name":request.user.username})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user_change_password(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Password Successfully updated")
                return HttpResponseRedirect('/profile/')
            else:
                messages.warning(request,"invalide password")
        else:
            fm=PasswordChangeForm(user=request.user)
        return render(request,'UserApp/change_pass.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/profile/')