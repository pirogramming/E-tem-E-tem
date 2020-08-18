from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from django.contrib.auth.decorators import login_required


def main(request):
    if request.user.id:
        # cart 비어있는 경우 로그인 시 오류나서 cart 만드는 코드가 이 부분에 있어야되니 지우지 말아주세요
        try:
            cart = Cart.objects.get(cart_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=request.user.id
            )
            cart.save()
        cart = Cart.objects.get(cart_id=request.user.id)
        cartitem = CartItem.objects.filter(cart=cart.id)
        count = cartitem.count()
    else:
        count = 0

    queryset = Powerpoint.objects.all().order_by("-download_count")
    colorset = ColorTag.objects.all()
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

    top5_template = Powerpoint.objects.all().order_by("-download_count")[:5]

    return render(request, 'main/main.html', {
        'cart_count': count,
        'template_list': template_list,
        'colorset': colorset,
        'p_range': p_range,
        'previous_block': previous_block,
        'next_block': next_block,
        'top5_template': top5_template,
    })


def color(request, id):
    if request.user.id:
        # cart 비어있는 경우 로그인 시 오류나서 cart 만드는 코드가 이 부분에 있어야되니 지우지 말아주세요
        try:
            cart = Cart.objects.get(cart_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=request.user.id
            )
            cart.save()
        cart = Cart.objects.get(cart_id=request.user.id)
        cartitem = CartItem.objects.filter(cart=cart.id)
        count = cartitem.count()
    else:
        count = 0

    colorset = ColorTag.objects.all()
    tag_list = PPT_tag.objects.filter(ppt_tag_id=id)
    ppt_list = []
    for tag in tag_list:
        ppt = Powerpoint.objects.filter(id=tag.template_id)
        ppt_list += ppt
    ppt_list = sorted(ppt_list, key=lambda tem: (tem.download_count), reverse=True)
    # ppt_list = tag_list.powerpoint.all()
    paginator = Paginator(ppt_list, 9)
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
    top5_template = Powerpoint.objects.all().order_by("-download_count")[:5]

    context = {
        'cart_count': count,
        "template_list": template_list,
        "colorset": colorset,
        'p_range': p_range,
        'previous_block': previous_block,
        'next_block': next_block,
        'top5_template': top5_template,
    }
    return render(request, "main/color.html", context)


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
    cartitems = CartItem.objects.filter(cart=cart.id)
    count = cartitems.count()
    print(count)
    cart.quantity = count
    cart.save()

    context = {
        'quantity': cart.quantity,
    }

    if not is_created:
        return HttpResponse("")

    print("******", is_created)

    return JsonResponse(context)


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
    queryset = DownloadItem.objects.filter(download=user_download_list.id)

    contexts = {
        "download_items": queryset,
    }
    return render(request, "main/download_list.html", contexts)


@login_required
def delete_cart_item(request, template_id):
    cart = Cart.objects.get(cart_id=request.user.id)
    CartItem.objects.get(cart=cart.id, template_id=template_id).delete()

    count = len(CartItem.objects.all())
    cart.quantity = count
    cart.save()

    return JsonResponse({})


def cart_item_delete(request, template_id):
    cart = Cart.objects.get(cart_id=request.user.id)
    CartItem.objects.get(cart=cart.id, template_id=template_id).delete()

    count = len(CartItem.objects.all())
    cart.quantity = count
    cart.save()

    return redirect('cart')


def download_count(request, template_id):
    template = Powerpoint.objects.get(pk=template_id)
    template.download_count += 1
    template.save()

    download_link = template.download_link
    context = {
        "download_link": download_link,
    }
    return JsonResponse({})

def myinfo(request):
    return render(request, "main/mypage.html")

@login_required
def reset_download_list(request):
    user_download_list = DownloadList.objects.get(user_id=request.user.id)
    download_item = DownloadItem.objects.filter(download=user_download_list.id).delete()
    user_download_list.save()

    return redirect('download_list')