from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail

from .forms import ContactForm
# Create your views here.

def home_page(request):
    return render(request, 'home_page.html', {})

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Getting in touch is easy!", 
        'content': "Fill this out so we can learn more about you and your needs",
        'form': contact_form,
    }
    content = request.POST.get('content')
    mail = request.POST.get('email', 'chetan.bhogade3899@gmail.com')
    if contact_form.is_valid():
        subject = 'Thank You from eComm Website - Chetan'
        message = f'Welcome to the eComm Website. This eCommerce website is build upon the Python Django Framework.\nYour message is : -  \n{content}'
        from_email = 'chetan.bhogade321@yahoo.com' 
        to_list = [mail]

        try:
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            print('Contact Page mail send successfully.')
        except Exception as e:
            print(f"Something Went Wrong... Error is : {e}")

        messages.success(request, "Your form is successfully submitted.")
    return render(request, 'contact_page.html', context=context)
