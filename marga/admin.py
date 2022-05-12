from django.contrib import admin
from .models import Product, Store, Url, Price

admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Url)
admin.site.register(Price)

