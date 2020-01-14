from django.shortcuts import render
from django.contrib import messages

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
    if contact_form.is_valid():
        messages.success(request, "Your form is successfully submitted.")
        print(contact_form.cleaned_data)
    return render(request, 'contact_page.html', context=context)
