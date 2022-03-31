from tkinter import CASCADE
from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=20, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_old = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_per_unit = models.CharField(max_length=50, null=True)
    link_to_picture = models.CharField(max_length=255, null=True)
    date_time_grab = models.DateTimeField(auto_now_add=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    discount_period = models.CharField(max_length=50, null=True)

class Url(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    url = models.URLField(max_length=200, null=True)