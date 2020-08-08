import time

from django.shortcuts import render, redirect
from .models import Powerpoint, Cart, CartItem, User, Download_List, Download_Item, Myinfo
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import IntegrityError
from django.contrib import messages

# Create your views here.

def main(request):

    queryset_list = Powerpoint.objects.all().order_by("id")
    paginator = Paginator(queryset_list, 9)  # posts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
    }
    # return render(request, "connect/main.html", context={'ppts': ppts})
    return render(request, "main/main.html", context)

# def myinfo(request):
#     return render(request, "main/mypage.html")

def add_one_to_cart(request, template_id):
    template = Powerpoint.objects.get(id=template_id)
    try:
        cart = Cart.objects.get(cart_id=request.user.username)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=request.user.username
        )
        cart.save()
    try:
        cart_item = CartItem.objects.create(
            template=template,
            cart=cart,
        )
        cart_item.save()
        return redirect('main')

    except IntegrityError:
        return redirect('main')


def show_cart_item(request):
    queryset = CartItem.objects.all()
    context = {
        "object_list": queryset,
    }
    # return render(request, "connect/main.html", context={'ppts': ppts})
    return render(request, "main/cart.html", context)

def add_one_to_download_list(request, templates_id):
    templates = Powerpoint.objects.get(id=templates_id)
    try:
        download = Download_List.objects.get(download_id=request.user.username)
    except Download_List.DoesNotExist:
        download = Download_List.objects.create(
            download_id=request.user.username
        )
        download.save()

    download_item = Download_Item.objects.create(
        templates=templates,
        download=download,
    )
    download_item.save()
    return redirect('main')

def show_download_list(request):
    querysets = Download_Item.objects.all()
    contexts = {
        "object_list": querysets,
    }
    return render(request, "main/download_list.html", contexts)

def cart_item_delete(request, template_id):
    cart_item = CartItem.objects.get(id=template_id)
    cart_item.delete()
    return redirect('cart')

def myinfo(request):
    return render(request, "main/mypage.html")