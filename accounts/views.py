from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SellerForm
from .models import Profile

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect('home')
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def become_seller(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = SellerForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.is_seller = True
        profile.save()
        messages.success(request, "You're now a seller!")
        return redirect('home')
    return render(request, 'accounts/become_seller.html', {'form': form})