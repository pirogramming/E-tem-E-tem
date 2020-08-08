from django.contrib import admin
from django.urls import path, include
from .views import main, add_one_to_cart, show_cart_item, show_download_list, add_one_to_download_list, delete_cart_item, myinfo
import login.views

urlpatterns = [
    path('', main, name='main'),
    path('add/<int:template_id>/', add_one_to_cart, name="add_one_to_cart"),
    path('cart/', show_cart_item, name="cart"),
    path('adds/<int:templates_id>/', add_one_to_download_list, name="add_one_to_download_list"),
    path('download_list/', show_download_list, name="download_list"),
    path('main/mypage/', myinfo, name="mypage"),
    path('remove/<int:template_id>/', delete_cart_item, name="cart_item_delete"),
]