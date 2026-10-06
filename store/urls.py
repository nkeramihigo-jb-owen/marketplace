from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
path('seller/add/', views.product_create, name='product_create'),
path('seller/<int:pk>/edit/', views.product_edit, name='product_edit'),
path('seller/<int:pk>/delete/', views.product_delete, name='product_delete'),
]