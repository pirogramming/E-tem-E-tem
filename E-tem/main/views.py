import time

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from django.contrib.auth.decorators import login_required


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

@login_required
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

    if not is_created:
        return HttpResponse("이미 장바구니에 존재하는 템플릿입니다.")

    print("******", is_created)
    return JsonResponse({})


@login_required
def show_cart_item(request):
    user_cart = Cart.objects.get(cart_id=request.user.id)
    queryset = CartItem.objects.filter(cart=user_cart.id)

    context = {
        "cart_items": queryset,
    }
    # return render(request, "connect/main.html", context={'ppts': ppts})
    return render(request, "main/cart.html", context)


@login_required
def add_one_to_download_list(request, templates_id):
    templates = Powerpoint.objects.get(id=templates_id)

    # download, _ = DownloadList.objects.get_or_create(user_num=request.user.id)

    try:
        download = DownloadList.objects.get(user_id=request.user.id)
    except DownloadList.DoesNotExist:
        download = DownloadList.objects.create(
            user_id=request.user.id
        )
        download.save()

    DownloadItem.objects.create(
        templates=templates,
        download=download,
    )

    # download_item = Download_Item(
    #     templates=templates,
    #     download=download
    # )
    # download_item.save()
    return redirect(reverse(download_count, kwargs={'template_id': templates_id}))


@login_required
def show_download_list(request):
    user_download_list = DownloadList.objects.get(user_id=request.user.id)
    queryset = DownloadItem.objects.filter(download = user_download_list.id)

    contexts = {
        "download_items": queryset,
    }
    return render(request, "main/download_list.html", contexts)


@login_required
def delete_cart_item(request, template_id):
    CartItem.objects.get(id=template_id).delete()
    return redirect('cart')


def download_count(request, template_id):
    template = Powerpoint.objects.get(pk=template_id)

    try:
        count = Count.objects.get(template_id=template_id)
        #count.template = template.objects.get(template_id=template_id)
        count.counts += 1
        count.save()


    except Count.DoesNotExist:
        #count = Count(template_id=template_id, count=1)

        Count.objects.create(
            template=template,
            counts=1,
        )

    # contexts = {
    #     "download": count,
    #     "count": count.counts,
    # }

    return render(request, '', {'download': template.download_link})


def myinfo(request):
    return render(request, "main/mypage.html")
