from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

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


# Getting different pages for different analytics pages 
def sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            start_date = timezone.now() - datetime.timedelta(days=7)
            qs = by_range(start_date=start_date)
            total = 0
            for i in qs:
                total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': total,
    }
    return render(request, "analytics/this-week-sales.html", context=context)

def last_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            start_date = timezone.now() - datetime.timedelta(days=14)
            end_date = timezone.now() - datetime.timedelta(days=7)
            qs = by_range(start_date=start_date, end_date=end_date)
            total = 0
            for i in qs:
                total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': total,
    }
    return render(request, "analytics/this-week-sales.html", context=context)


def three_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            start_date = timezone.now() - datetime.timedelta(days=3*7)
            end_date = timezone.now() - datetime.timedelta(days=2*7)
            qs = by_range(start_date=start_date, end_date=end_date)
            total = 0
            for i in qs:
                total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': total,
    }
    return render(request, "analytics/this-week-sales.html", context=context)


def four_week_sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            start_date = timezone.now() - datetime.timedelta(days=5*7)
            end_date = timezone.now() - datetime.timedelta(days=3*7)
            qs = by_range(start_date=start_date, end_date=end_date)
            total = 0
            for i in qs:
                total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': total,
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
            print(f"From View: dict: {my_dict}")

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



# Grabbing the all ajax calls from chart.js to render the chart properly
def sales_ajax_view(request):
    data = {}
    if request.user.is_superuser:

        if request.GET.get("type") == "thisWeek":
            labels, totals = weeks_age_sales(no_of_weeks=0)
        elif request.GET.get("type") == "lastWeek":
            labels, totals = weeks_age_sales(no_of_weeks=1)
        elif request.GET.get("type") == "threeWeek":
            labels, totals = weeks_age_sales(no_of_weeks=3)
        elif request.GET.get("type") == "fourWeek":
            labels, totals = weeks_age_sales(no_of_weeks=4)
        elif request.GET.get("type") == "productAnalytics":
            labels, totals = product_ajax_details()
        else:
            labels, totals = [], []

        data['labels'] = labels[::-1] # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['data'] = totals[::-1]
        

    else:
        messages.warning(request, "You cannot access this page. Please Login as Admin!")
        return redirect("account:login")

    return JsonResponse(data=data)

