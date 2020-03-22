from django.shortcuts import render
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from .forms import ContactForm
from products.models import Product
from analytics.models import ObjectViewed
# Create your views here.

def home_page(request):
    qs = Product.objects.all()[::-1][:9]

    c_type = ContentType.objects.get_for_model(Product)
    prods_qs = ObjectViewed.objects.filter(content_type=c_type)
    test_list = [x.content_object for x in prods_qs]
    my_dict = {i:test_list.count(i) for i in test_list}
    popular_product = max(my_dict, key=my_dict.get)

    context = {
        "Products": qs,
        "popular_product": popular_product
    }
    

    return render(request, 'home_page.html', context=context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Getting in touch is easy!", 
        'content': "Fill this out so we can learn more about you and your needs",
        'form': contact_form,
    }
    full_name = request.POST.get('full_name')
    customer_email = request.POST.get('email')
    content = request.POST.get('content')

    receiver_email = 'chetanbhogade999@gmail.com'
    if contact_form.is_valid():
        subject = 'Contact Form Submission - from eComm Website'
        message = f'Contact Form Submission.\n\nCustomer Full Name: - {full_name}\nCustomer Email: - {customer_email}\nCustomer Query: - {content} '
        from_email = 'chetan.bhogade321@yahoo.com' 
        to_list = [receiver_email]

        try:
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            print('Contact Page mail send successfully.')
        except Exception as e:
            print(f"Something Went Wrong While Sending Email... Error is : {e}")

        messages.success(request, "Your form is successfully submitted.")
    return render(request, 'contact_page.html', context=context)
