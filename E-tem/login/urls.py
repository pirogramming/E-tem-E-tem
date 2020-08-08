from django.contrib import admin
from django.urls import path, include
from .views import loginhome
import login.views

urlpatterns = [
    path('', loginhome, name='loginhome'),
    ]