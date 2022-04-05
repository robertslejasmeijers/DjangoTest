"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from marga import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("api/products", views.Productsview)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("grab_barbora/", views.grab_barbora),
    path("grab_rimi/", views.grab_rimi),
    path("searchdb/", views.searchdb, name="searchdb"),
    path("addurltodb/", views.addurltodb),
    path("addinfotodb/", views.addinfotodb),
    path("addedurls/", views.addedurls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    
]

urlpatterns += router.urls