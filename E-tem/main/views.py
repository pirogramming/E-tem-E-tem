from django.shortcuts import render, redirect
from .models import Powerpoint, Cart, CartItem, User
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

#___________________________________________________

#def _cart_id(request):
#    cart = request.session.session_key
#    if not cart:
#        cart = request.session.create()
#    return cart

def add_one_to_cart(request, template_id):
    template = Powerpoint.objects.get(id=template_id)
    try:
        cart = Cart.objects.get(cart_id=request.user.username)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=request.user.username
        )
        cart.save()

    cart_item = CartItem.objects.create(
        template = template,
        cart = cart
    )
    cart_item.save()
    return redirect('main')

def show_cart_item(request):
    queryset = CartItem.objects.all()
    context = {
        "object_list": queryset,
    }
    # return render(request, "connect/main.html", context={'ppts': ppts})
    return render(request, "main/cart.html", context)