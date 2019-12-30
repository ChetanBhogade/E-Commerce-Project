from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    return render(request, 'home_page.html', {})

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Getting in touch is easy!", 
        'content': "Fill this out so we can learn more about you and your needs",
        'form': contact_form,
    }
    if contact_form.is_valid():
        messages.success(request, "Your form is successfully submitted.")
        print(contact_form.cleaned_data)
    return render(request, 'contact_page.html', context=context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'title': "Please Login!", 
        'form': form,
    }
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("User Logged in : ", request.user.is_authenticated)
        # Redirect to a success page.
        messages.success(request, "Login Successful.")
        return redirect('/')
    else:
        # Return an 'invalid login' error message.
        print("Error...")
    
    return render(request, 'auth/login.html', context=context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'title': "Register Yourself", 
        'form': form,
    }
    username = request.POST.get('username')
    email    = request.POST.get('email')
    password = request.POST.get('password')
    if form.is_valid():
        user = User.objects.create_user(username=username, email=email, password=password)
        print("User created : ", user)
        messages.success(request, f"User: - '{user}' successfully Added.")
        print(form.cleaned_data)
    return render(request, 'auth/register.html', context=context)


def logout_page(request):
    if request.user.is_authenticated:
        print("User logged out : ", request.user)
        messages.success(request, "Logged Out ")
        logout(request)
        return redirect("/login")
    else:
        messages.error(request, "Logging out failed...")
