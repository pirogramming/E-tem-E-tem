import time

from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

from django.db import IntegrityError
from django.contrib import messages


# Create your views here.


def main(request):
    queryset = Powerpoint.objects.all().order_by("id")
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page')
    template_list = paginator.get_page(page)
    page_range = 5
    try:
        current_block = math.ceil(int(page) / page_range)
    except:
        page = 1
        current_block = math.ceil(int(page) / page_range)
    start_block = (current_block - 1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    previous_block = int(page) - 5
    next_block = int(page) + 5
    return render(request, 'main/main.html', {
        'template_list': template_list,
        'p_range': p_range,
        'previous_block': previous_block,
        'next_block': next_block,
    })


def add_one_to_cart(request, template_id):
    template = Powerpoint.objects.get(id=template_id)
    try:
        cart = Cart.objects.get(cart_id=request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=request.user.id
        )
        cart.save()

    cart_item, is_created = CartItem.objects.get_or_create(
        template=template,
        cart=cart,
    )
    return redirect('main')
    # try:
    #
    #     cart_item = CartItem.objects.create(
    #         template=template,
    #         cart=cart,
    #     )
    #     cart_item.save()
    #     return redirect('main')
    #
    # except IntegrityError:
    #     return redirect('main')


def show_cart_item(request):
    user_cart = Cart.objects.get(cart_id=request.user.id)
    queryset = CartItem.objects.filter(cart=user_cart.id)

    context = {
        "cart_items": queryset,
    }
    # return render(request, "connect/main.html", context={'ppts': ppts})
    return render(request, "main/cart.html", context)


def add_one_to_download_list(request, templates_id):
    templates = Powerpoint.objects.get(id=templates_id)
    download, _ = DownloadList.objects.get_or_create(user_id=request.user.id)
    # try:
    #     download = Download_List.objects.get(download_id=request.user.username)
    # except Download_List.DoesNotExist:
    #     download = Download_List.objects.create(
    #         download_id=request.user.username
    #     )
    #     download.save()

    DownloadItem.objects.create(
        templates=templates,
        download=download,
    )

    # download_item = Download_Item(
    #     templates=templates,
    #     download=download
    # )
    # download_item.save()
    return redirect('main')


def show_download_list(request):
    queryset = DownloadItem.objects.all()
    # 이름 변경??
    contexts = {
        "object_list": queryset,
    }
    return render(request, "main/download_list.html", contexts)


def delete_cart_item(request, template_id):
    CartItem.objects.delete(id=template_id)
    return redirect('cart')


def myinfo(request):
    return render(request, "main/mypage.html")
