from decimal import Decimal
from .models import Product

CART_KEY = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_KEY, {})

    def _save(self):
        self.session.modified = True

    def add(self, product_id, quantity=1):
        pid = str(product_id)
        self.cart[pid] = min(self.cart.get(pid, 0) + quantity, 99)
        self._save()

    def set(self, product_id, quantity):
        pid = str(product_id)
        if quantity <= 0:
            self.cart.pop(pid, None)
        else:
            self.cart[pid] = min(quantity, 99)
        self._save()

    def remove(self, product_id):
        self.cart.pop(str(product_id), None)
        self._save()

    def clear(self):
        self.session[CART_KEY] = {}
        self._save()

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys(), is_active=True).select_related('seller__profile')
        for product in products:
            qty = self.cart[str(product.id)]
            yield {'product': product, 'quantity': qty, 'subtotal': product.price * qty}

    def __len__(self):
        return sum(self.cart.values())

    def total(self):
        return sum((item['subtotal'] for item in self), Decimal('0'))