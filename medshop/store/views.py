from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import * 


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.itemsorder_set.all()
        itemsInCart = order.getCartItems
    else:
        order = {'getCartTotal':0, 'getCartItems':0, 'shipping': False}
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
        order = {'getCartTotal':0, 'getCartItems':0, 'shipping': False}
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
        items = []
        order = {'getCartTotal':0, 'getCartItems': 0, }
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


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.getCartTotal:
		order.complete = True
	order.save()

	if order.shipping == True:
		Shipping.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)