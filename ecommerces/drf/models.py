# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


# Create your models here.

STATUS_CHOICES = (
    ('Order Placed', 'Order Placed'),
    ('Order Accepted', 'Order Accepted'),
    ('Order Canceled', 'Order Canceled')
)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True,max_length=30)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

"""
Custom User models
"""
class CustomUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customuser')
    role = models.CharField(max_length=5)


class UserRole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_role')
    title = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'user_role'

    def __str__(self):
        return self.title

class Product(models.Model):
    product_name = models.CharField(max_length=30, null=True, blank=True)
    price = models.DecimalField(max_digits=13,decimal_places=2)
    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='order')
    customer_or_vendor = models.ForeignKey(UserRole, db_column='customerVendorRoleId_id')
    order_status = models.CharField(max_length=50, default='Order Placed', choices=STATUS_CHOICES)  # Order Placed, Order Accepted, Order Canceled
    class Meta:
        db_table = 'order'
    def __str__(self):
        return self.order_status

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='pi_product')
    quantity = models.DecimalField(max_digits=11,decimal_places=2)
    price = models.DecimalField(max_digits=13,decimal_places=2)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='oi_product')
    class Meta:
        db_table = 'orderItem'

    def __str__(self):
        return self.product

    def __str__(self):
        return "{0} of {1}".format(self.quantity,self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()