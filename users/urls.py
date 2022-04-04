from django.urls import path
from marga import views
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
]
