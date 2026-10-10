from django import forms
from .models import Order, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'category', 'description', 'price', 'image', 'is_active')

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'address', 'city')

from .models import Product, Order, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience...'})}    