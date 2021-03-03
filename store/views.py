import json
import datetime

from .models import *

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.models import User
# import csrf so that csrf token is passed
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# cartItems created in each view so that the no of carts are displayed. This is manual process but rest api can be used to make it dynamic


def search(request):

    return render(request, 'store/search.html')


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # child data(orderitem) and parent(order)...the orderiem with respective order is stored
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # child data(orderitem) and parent(order)...the orderiem with respective order is stored
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # if there is no cookie name cart there will be an KeyError(bug) to fix this exception,
        # following code is written
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:', cart)
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            # updating order values so that guest user can add to cart
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.imageUrl
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # child data(orderitem) and parent(order)...the orderiem with respective order is stored
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # checking if the order exists else order gets created
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    # checking if orderItem exists else orderItem gets created
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("It was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        # Note: in db there is shopping address not shipping
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                state=data['shippingInfo']['state'],
                zipcode=data['shippingInfo']['zipcode'],
            )

    else:
        print("User is not logged in")
    return JsonResponse("Payment Complete", safe=False)
