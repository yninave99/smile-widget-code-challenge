from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path('', views.index),
    path('api/getproductprice', views.get_product_price),
    path('api/getproductcode/', views.get_product_code),
    path('api/getgiftcardcode/', views.get_gift_code)
]
