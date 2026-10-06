from django.db.models import Q
from .models import Product, Category
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

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
    return render(request, 'store/product_detail.html', {'product': product})

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
