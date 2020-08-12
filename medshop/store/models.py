from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True)
    surname = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True)
    company = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=500, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    #function to fix image error when epmty 
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
 
    @property
    def getCartTotal(self):
        ordered = self.itemsorder_set.all()
        total = sum([item.calcTotal for item in ordered])
        return total 

    @property
    def getCartItems(self):
        ordered = self.itemsorder_set.all()
        total = sum([item.quantity for item in ordered])
        return total 

    @property
    def shipping(self):
        shipping = False
        itemsorder = self.itemsorder_set.all()
        return shipping 


class ItemsOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def calcTotal(self):
        total = self.product.price * self.quantity
        return total 

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    state = models.CharField(max_length=150, null=True)
    zipcode = models.CharField(max_length=150, null=True)
    date_added = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.address

    
    
    

    