from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math


def main_color(request):
    queryset = Powerpoint.objects.all().order_by("id")
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
    return render(request, 'main/main_color.html', {
        'template_list': template_list,
        'colorset': colorset,
        'p_range': p_range,
        'previous_block': previous_block,
        'next_block': next_block,
    })


def color(request, id):
    colorset = ColorTag.objects.all()
    tag_list = PPT_tag.objects.filter(ppt_tag_id=id)
    ppt_list = []
    for tag in tag_list:
        ppt = Powerpoint.objects.get(id=tag.template_id)
        ppt_list.append(ppt)
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
    context = {
        "ppt_items": template_list,
        "colorset": colorset,
        'p_range': p_range,
        'previous_block': previous_block,
        'next_block': next_block,
    }
    return render(request, "main/color.html", context)
