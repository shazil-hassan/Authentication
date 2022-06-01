# from binascii import rledecode_hqx
# from datetime import date
# from traceback import format_exc
from ast import Not
from asyncio.windows_events import NULL
import email
from email import message

from sre_constants import SUCCESS
from urllib import response
from django import views
from django.http import HttpResponse

from .models import * 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# from login import tokens
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .tokens import account_activation_token
# from django.contrib.auth.tokens import PasswordResetTokenGenerator  

from django.shortcuts import render ,HttpResponse,redirect,HttpResponseRedirect
from .forms import UserForm,UpdateUserForm,ChangeUserPassword,ResetPass,Admin_editUser
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index( request):
    if User.is_authenticated:
        if request.user.is_superuser== True:
            user=User.objects.all()
            return render(request,'admin_base.html',{'user':user})
        else:
            return render(request,'index.html')



def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.role=2
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            })
      
            to_email = form.cleaned_data.get('email')
         
            sent_email(subject, message ,to_email)
            # email.send()

            # login(request,user)
            messages.success(request, "Account Activation Email has been sent to your Email ." )
            return redirect('index')
    
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserForm()
    return render (request=request, template_name="signup.html",context={"signup_form":form})


def Activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if  user is not None:
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('LogIn')


def log_in(request):
    
    if request.method == "POST":
     
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def updateUser(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm=UpdateUserForm(request.POST,request.FILES,instance=request.user)
            if fm.is_valid():
                messages.success(request, "Updateed successfully.")
                fm.save()
                return redirect('update')
                
        else:
            fm=UpdateUserForm(instance=request.user)
        return render(request,template_name="update_profile.html",context={'name': request.user,'form':fm})
    else:
        return redirect('LogIn')

def changepassword(request):
  
        if request.method == "POST":
            fm=ChangeUserPassword(request.user,request.POST)
            if fm.is_valid():
               
                user=fm.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password Change successfully.")
                return redirect('index')
        else:
            fm=ChangeUserPassword(request.user)
        return render(request,'changepass.html',{'form':fm})


def forgotPass(request):
    if request.method == "POST":
        to_email=request.POST.get('email')
        user=User.objects.get(email=to_email)
        if user is None:
            return redirect("ResetPassword")
        
        subject='Reset Password'
        current_site = get_current_site(request)
        subject = 'Activate your account'
        message = render_to_string('reset.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
        })
        sent_email(subject, message, to_email)
    
    return render(request,'forgotPass.html')

def ResetPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        email = UserModel._default_manager.get(id=uid)
        return redirect("ResetConfirm",  email)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def ResetConfirm(request, email):
    if request.method=="POST":
        fm = ResetPass(request.POST)
        getpassword = request.POST['password1']
        if fm.is_valid():
            user = User.objects.get(email=email)
            if user:
                user.set_password(getpassword)  # replace with your real password
                user.save()
            return redirect("LogIn")
        else:
    
            return redirect("ResetConfirm")
    else:
          fm=ResetPass(request.POST)        

    return render(request,'reset_confirm.html',{"form":fm, 'email': email})

def logout_req(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("LogIn")

def sent_email(subject,html_content,to_email):
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        [to_email]
    ) 
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@csrf_exempt
def admin_edit(request):
    if request.method=="POST":
        id=request.POST.get('id')

        user = User.objects.get(id=id)
        if user:
            res = user
        else:
            res = "No Data"

    return HttpResponse(res)

# def  Delete_user(request):
#     if request.method=="POST":  
#         user_id=request.POST.get('user_id') 
#         user=request.user
#         if user is not "":
#             user.delete()

