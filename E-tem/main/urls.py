from django.contrib import admin
from django.urls import path, include
from .views import main, add_one_to_cart, show_cart_item
import login.views

urlpatterns = [
    path('', login.views.loginhome, name='E-tem'),
    path('main/', main, name='main'),
    path('add/<int:template_id>/', add_one_to_cart, name="add_one_to_cart"),
    path('cart/', show_cart_item, name="cart")
]