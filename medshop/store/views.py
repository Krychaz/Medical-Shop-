from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.itemsorder_set.all()
        itemsInCart = order.getCartItems
    else:
        order = {'getCartTotal':0, 'getCartItems':0}
        items = []
        itemsInCart = order['getCartItems']

    products = Product.objects.all()
    context = {'products' :products, 'itemsInCart': itemsInCart}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.itemsorder_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal':0, 'getCartItems':0}
        cartItems = order['getCartItems']
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.itemsorder_set.all()
        cartItems = order.getCartItems
    else:
        order = {'getCartTotal':0, 'getCartItems':0}
        items = []
        order = {'getCartTotal':0, 'getCartItems': 0}
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    itemsOrder, created = ItemsOrder.objects.get_or_create(order=order, product=product)

    if action == 'add':
        itemsOrder.quantity = (itemsOrder.quantity + 1)
    elif action == 'remove':
        itemsOrder.quantity = (itemsOrder.quantity - 1)
    
    itemsOrder.save()

    if itemsOrder.quantity <= 0:
        itemsOrder.delete()

    return JsonResponse('Item was added', safe=False)