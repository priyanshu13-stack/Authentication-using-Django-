# Project created by Priyanshu Verma 
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,render
from login import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['Username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request,"Username already exists!")
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters!")

        if pass1!=pass2:
            messages.error(request,"Passwords didn't match!")
            
        if not username.isalnum():
            messages.error(request,"Username must be alphanumeric!")
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created!. We have sent you a confirmation email, please confirm your email in order to activate your account!")

        # welcome email
        subject = "Welcome to GFG Login!!"
        message = "Hello! " + myuser.first_name +"!! \n" + "Welcome to GFG \n Thank you for visiting our website! \n We have also sent you an confirmation email, Please confirm your email address in order to activate your account. \n\n Thanking you! "  
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently = True)

        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['Username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Incorrect Credentials!")
            return redirect('home')

    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('home')
