from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from products.models import Product
from .models import ObjectViewed
from orders.models import Order

import random
import datetime
# Create your views here.


# Specific User History Page: - Only For customers
def user_product_history(request):
    if request.user.is_authenticated:
        c_type = ContentType.objects.get_for_model(Product)
        qs = ObjectViewed.objects.filter(content_type=c_type, user=request.user)
        test_list = [x.content_object.title[:20] for x in qs]
        print(list(set(test_list)))
        my_dict = {i:test_list.count(i) for i in test_list}
        print(my_dict)
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        "qs": qs,
    }
    return render(request, "analytics/user-product-history.html", context=context)


def product_total_views():
    c_type = ContentType.objects.get_for_model(Product)
    qs = ObjectViewed.objects.filter(content_type=c_type)
    prod_list = [x.content_object.title for x in qs]
    prod_views_dict = {i:prod_list.count(i) for i in prod_list}
    return prod_views_dict





# Calculating and adjusting the datetime fields for Orders analytics views
def by_range(start_date, end_date=None):
    if end_date is None:
        return Order.objects.filter(updated__gte=start_date)
    return Order.objects.filter(updated__gte=start_date).filter(updated__lte=end_date)


def weeks_age_sales(no_of_weeks):
    days_ago_start = no_of_weeks * 7
    labels = []
    data = []
    for day in range(days_ago_start, days_ago_start+7):
        start_date = timezone.now() - datetime.timedelta(days=day)
        qs = Order.objects.filter(updated__day=start_date.day, updated__month=start_date.month)
        total = 0
        for i in qs:
            total += i.total
        labels.append(start_date.strftime("%A"))
        data.append(total)
    return labels, data

def get_sales_data(start_date):
    list_of_orders = []
    for day in range(start_date, start_date+7):
        start_date = timezone.now() - datetime.timedelta(days=day)
        qs = Order.objects.filter(updated__day=start_date.day, updated__month=start_date.month)
        for i in qs:
            list_of_orders.append(i)
    return list_of_orders



# Getting different pages for different analytics pages 
def sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            qs = get_sales_data(start_date=0)

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': 0,
    }
    return render(request, "analytics/this-week-sales.html", context=context)

def last_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            qs = get_sales_data(start_date=7)

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': 0,
    }
    return render(request, "analytics/this-week-sales.html", context=context)


def three_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            qs = get_sales_data(start_date=14)

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': 0,
    }
    return render(request, "analytics/this-week-sales.html", context=context)


def four_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            qs = get_sales_data(start_date=21)

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': 0,
    }
    return render(request, "analytics/this-week-sales.html", context=context)



# For Product analytics page 
def product_analytics_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            c_type = ContentType.objects.get_for_model(Product)
            qs = ObjectViewed.objects.filter(content_type=c_type)
            test_list = [x.content_object.title for x in qs]
            my_dict = {i:test_list.count(i) for i in test_list}
            # print(f"From View: dict: {my_dict}")

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        "qs": qs, 
        "product_list": my_dict,
    }
    return render(request, "analytics/product-analytics.html", context=context)

def product_ajax_details():

    c_type = ContentType.objects.get_for_model(Product)
    qs = ObjectViewed.objects.filter(content_type=c_type)
    test_list = [x.content_object.title for x in qs]
    my_dict = {i:test_list.count(i) for i in test_list}

    labels = [i for i in my_dict.keys()]
    data = [i for i in my_dict.values()]
    return labels, data


# For Customer Analytics Page
def get_user_data():
    all_users = User.objects.all()
    user_name = []
    user_total = []
    for user in all_users:
        qs = Order.objects.filter(status='Paid', billing_profile__user = user)
        total = 0
        for i in qs:
            total += i.total
        user_name.append(str(user))
        user_total.append(total)
    return user_name, user_total


def customers_analytics_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_name, user_total = get_user_data()
            data = dict(zip(user_name, user_total))

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        "cust_data": data
    }
    return render(request, "analytics/user-analytics.html", context=context)



# Grabbing the all ajax calls from chart.js to render the chart properly
def sales_ajax_view(request):
    data = {}
    if request.user.is_superuser:

        if request.GET.get("type") == "thisWeek":
            labels, totals = weeks_age_sales(no_of_weeks=0)
        elif request.GET.get("type") == "lastWeek":
            labels, totals = weeks_age_sales(no_of_weeks=1)
        elif request.GET.get("type") == "threeWeek":
            labels, totals = weeks_age_sales(no_of_weeks=2)
        elif request.GET.get("type") == "fourWeek":
            labels, totals = weeks_age_sales(no_of_weeks=3)
        elif request.GET.get("type") == "productAnalytics":
            labels, totals = product_ajax_details()
        elif request.GET.get("type") == "UserAnalytics":
            labels, totals = get_user_data()
        else:
            labels, totals = [], []

        data['labels'] = labels[::-1] # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['data'] = totals[::-1]
        

    else:
        messages.warning(request, "You cannot access this page. Please Login as Admin!")
        return redirect("account:login")

    return JsonResponse(data=data)



def advertise_product_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            c_type = ContentType.objects.get_for_model(Product)
            prods_qs = ObjectViewed.objects.filter(content_type=c_type)
            test_list = [x.content_object for x in prods_qs]
            my_dict = {i:test_list.count(i) for i in test_list}
            popular_product = max(my_dict, key=my_dict.get)

            if request.method == "POST":
                subject = request.POST.get('subject')
                description = request.POST.get('content')
                all_users = User.objects.all()
                receivers_list = []
                for user in all_users:
                    receivers_list.append(user.email)
                from_email = 'chetan.bhogade321@yahoo.com'
                message_body = f"{description}\n---------------------------------\nProduct Name: - {popular_product.title}\nProduct Description: - {popular_product.description}\nProduct Price: - {popular_product.price}/-\n---------------------------------\nView This Product: - http://127.0.0.1:8000/products/elitera-sunglasses/"

                print(f"List of all users mail: - {receivers_list}")
                try:
                    send_mail(subject, message_body, from_email, receivers_list, fail_silently=False)
                    messages.success(request, "Email send successfully.")
                    print("Email send successfully.")
                except Exception as e:
                    messages.error(request, "Something Went Wrong While Sending Emails.")
                    print(f"Something Went Wrong While Sending Email... Error is : {e}")

            context = {
                "popular_product": popular_product
            }
        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    return render(request, "analytics/product-advertisement-page.html", context=context)


