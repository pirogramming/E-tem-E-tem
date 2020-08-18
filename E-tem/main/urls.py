from django.urls import path
from .views import *


urlpatterns = [
    path('', main, name='main'),
    path('add/<int:template_id>/', add_one_to_cart, name="add_one_to_cart"),
    path('cart/', show_cart_item, name="cart"),
    path('adds/<int:templates_id>/', add_one_to_download_list, name="add_one_to_download_list"),
    path('download_list/', show_download_list, name="download_list"),
    path('main/mypage/', myinfo, name="mypage"),
    path('delete/<int:template_id>/', cart_item_delete, name="cart_item_delete"),
    path('remove/<int:template_id>/', delete_cart_item, name="delete_cart_item"),
    path('count/<int:template_id>/', download_count, name="download_count"),
    path('color/<int:id>/', color, name="color"),
]
