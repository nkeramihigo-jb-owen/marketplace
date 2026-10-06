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
path('cart/', views.cart_detail, name='cart'),
path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
path('cart/update/<int:pk>/', views.cart_update, name='cart_update'),
path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
path('checkout/', views.checkout, name='checkout'),
path('orders/', views.my_orders, name='my_orders'),
path('orders/<int:pk>/success/', views.order_success, name='order_success'),
path('seller/orders/', views.seller_orders, name='seller_orders'),
path('seller/orders/<int:pk>/status/', views.seller_item_status, name='seller_item_status'),
]