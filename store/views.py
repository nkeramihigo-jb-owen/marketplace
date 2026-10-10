from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from .models import Product, Category
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import ProductForm, CheckoutForm, ReviewForm
from .models import Product, Category, Order, OrderItem,Review

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    q = request.GET.get('q')
    category = request.GET.get('category')
    if q:
        products = products.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        products = products.filter(category__slug=category)

    return render(request, 'store/product_list.html', {
        'products': products, 'categories': categories, 'q': q or '', 'active_category': category,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.select_related('user')
    stats = reviews.aggregate(avg=Avg('rating'), count=Count('id'))

    form = None
    if request.user.is_authenticated and request.user != product.seller:
        has_bought = OrderItem.objects.filter(product=product, order__buyer=request.user).exists()
        if has_bought:
            existing = reviews.filter(user=request.user).first()
            form = ReviewForm(instance=existing)

    return render(request, 'store/product_detail.html', {
        'product': product, 'reviews': reviews, 'stats': stats, 'form': form,
    })
def seller_required(view):
    """Only logged-in users with a seller profile can pass."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_seller:
            messages.info(request, "Open a shop first to start selling.")
            return redirect('become_seller')
        return view(request, *args, **kwargs)
    return login_required(wrapper)

@seller_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/seller_dashboard.html', {'products': products})

@seller_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        messages.success(request, "Product added.")
        return redirect('seller_dashboard')
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add product'})

@seller_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product updated.")
        return redirect('seller_dashboard')
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit product', 'product': product})

@seller_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('seller_dashboard')
    return render(request, 'store/product_confirm_delete.html', {'product': product})

def _qty(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'items': list(cart), 'total': cart.total()})

@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if request.user.is_authenticated and product.seller_id == request.user.id:
        messages.error(request, "You can't buy your own product.")
        return redirect('product_detail', pk=pk)
    Cart(request).add(product.pk, max(_qty(request.POST.get('quantity')), 1))
    messages.success(request, f'"{product.title}" added to your cart.')
    return redirect('cart')

@require_POST
def cart_update(request, pk):
    cart = Cart(request)
    cart.set(pk, _qty(request.POST.get('quantity'), 1))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item = next((i for i in cart if i['product'].pk == pk), None)
        return JsonResponse({
            'removed': item is None,
            'subtotal': str(item['subtotal']) if item else '0',
            'total': str(cart.total()),
            'count': len(cart),
        })
    return redirect('cart')

@require_POST
def cart_remove(request, pk):
    Cart(request).remove(pk)
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect('product_list')

    form = CheckoutForm(request.POST or None, initial={
        'full_name': request.user.get_full_name(),
        'phone': request.user.profile.phone,
    })
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            for item in items:
                p = item['product']
                OrderItem.objects.create(
                    order=order, product=p, seller=p.seller,
                    title=p.title, price=p.price, quantity=item['quantity'],
                )
        cart.clear()
        return redirect('order_success', pk=order.pk)

    return render(request, 'store/checkout.html', {'form': form, 'items': items, 'total': cart.total()})

@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items')
    return render(request, 'store/my_orders.html', {'orders': orders})

@seller_required
def seller_orders(request):
    items = OrderItem.objects.filter(seller=request.user).select_related('order')
    return render(request, 'store/seller_orders.html', {'items': items})

@seller_required
@require_POST
def seller_item_status(request, pk):
    item = get_object_or_404(OrderItem, pk=pk, seller=request.user)
    status = request.POST.get('status')
    if status in dict(OrderItem.STATUS):
        item.status = status
        item.save()
        messages.success(request, "Status updated.")
    return redirect('seller_orders')

@login_required
@require_POST
def review_submit(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    has_bought = OrderItem.objects.filter(product=product, order__buyer=request.user).exists()
    if not has_bought:
        messages.error(request, "Only customers who bought this product can review it.")
        return redirect('product_detail', pk=pk)

    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.update_or_create(
            product=product, user=request.user, defaults=form.cleaned_data,
        )
        messages.success(request, "Thanks for your review!")
    return redirect('product_detail', pk=pk)

def shop_detail(request, username):
    seller = get_object_or_404(User, username=username, profile__is_seller=True)
    products = Product.objects.filter(seller=seller, is_active=True)
    return render(request, 'store/shop_detail.html', {'seller': seller, 'products': products})