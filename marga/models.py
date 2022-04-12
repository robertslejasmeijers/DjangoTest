from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    RIMI_ID = 1
    BARBORA_ID = 2
    SIRSNIGA_ID = 3


        
class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    link_to_picture = models.URLField(max_length=255, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ('name', )
    def __str__(self):
        return self.name    
    

class Price(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_old = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_per_unit = models.CharField(max_length=50, null=True)
    discount_period = models.CharField(max_length=50, null=True)
    date_time_grab = models.DateTimeField(auto_now_add=True, null=True)
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ('price', )

class Url(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    url = models.URLField(max_length=200, null=True)

print ("BEFORE: Store exists")
try:
    print ("TRY: Store exists")
    if not Store.objects.exists(): #prepopulate the database with some stores
        print ("Pievienojam Store")
        Store.objects.create(name="Rimi")
        Store.objects.create(name="Barbora")
        Store.objects.create(name="Sirsniga")
except:
    pass
