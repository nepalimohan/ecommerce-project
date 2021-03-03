from django.shortcuts import render
from store.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
# Create your views here.


def loginuser(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # child data(orderitem) and parent(order)...the orderiem with respective order is stored
        # items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'cartItems': cartItems, 'shipping': False}
    return render(request, "accounts/loginuser.html", context)


def signupuser(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # child data(orderitem) and parent(order)...the orderiem with respective order is stored
        # items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'cartItems': cartItems, 'shipping': False}
    return render(request, "accounts/signupuser.html", context)
