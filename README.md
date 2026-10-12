# Marketplace

A multi-seller online marketplace built with **Django**, **HTML**, **CSS** and **JavaScript**. Anyone can sign up and buy, and any user can open a shop and sell their own products. Think of a small Etsy or Jumia.

## Features

**Buyers**
- Browse products, search by keyword, and filter by category
- Session-based shopping cart with live quantity updates (no page reload)
- Checkout with delivery details (pay on delivery for now)
- Order history with per-item delivery status
- Rate and review products they have bought (one review per product, editable)

**Sellers**
- "Become a seller" flow with a shop name, phone and bio
- Seller dashboard to add, edit, hide and delete products with image uploads and live image preview
- Orders received page, showing only the seller's own items, with status updates (Pending, Shipped, Delivered)
- Public shop page at `/shop/<username>/`

**Platform**
- Orders can contain items from many different sellers; each seller only sees and manages their own items
- Ownership checks on every seller action, so nobody can edit another seller's products or orders
- Order items store a snapshot of the title and price, so old orders stay correct if a product changes
- Django admin for managing categories, products, orders and reviews

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Database | SQLite (development) |
| Frontend | Django templates, HTML, CSS, vanilla JavaScript |
| Images | Pillow (uploads saved to `media/`) |

## Project structure

```
marketplace/
├── manage.py
├── config/            # project settings and root URLs
├── accounts/          # profiles, sign up, seller onboarding
├── store/             # products, cart, orders, reviews, seller dashboard
├── templates/         # all HTML templates (base.html, registration/, accounts/, store/)
├── static/            # css/ and js/
└── media/             # uploaded product images (created automatically)
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/nkeramihigo-jb-owen/marketplace.git
cd marketplace
```

### 2. Create and activate a virtual environment

Using pipenv:

```bash
pipenv install django pillow
pipenv shell
```

Or using venv:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux
pip install django pillow
```

### 3. Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

### 5. Add starter data

1. Go to http://127.0.0.1:8000/admin and log in with your superuser.
2. Add some **Categories** (the slug fills in automatically).
3. Sign up a normal user at `/accounts/signup/`, click **Become a seller**, then add products from **My shop**.

Or create categories quickly from the shell:

```bash
python manage.py shell
```

```python
from django.utils.text import slugify
from store.models import Category

for name in ["Electronics", "Phones & Tablets", "Fashion & Clothing", "Home & Kitchen",
             "Beauty & Health", "Groceries & Food", "Books & Stationery", "Sports & Outdoors"]:
    Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
```

## Key URLs

| URL | Purpose |
|---|---|
| `/` | Home page |
| `/products/` | Product list with search and category filter |
| `/products/<id>/` | Product detail and reviews |
| `/shop/<username>/` | Public seller shop page |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout |
| `/orders/` | Buyer's order history |
| `/seller/` | Seller dashboard |
| `/seller/orders/` | Orders received by a seller |
| `/accounts/signup/`, `/accounts/login/` | Authentication |
| `/admin/` | Django admin |

## Data model overview

- **Profile**: one-to-one with `User`; holds `is_seller`, shop name, phone and bio
- **Category** and **Product**: each product belongs to a seller and a category
- **Order** and **OrderItem**: one order per checkout; each item records its own seller and delivery status
- **Review**: one per user per product, only allowed after a purchase

## Roadmap

- [ ] Stock quantity and overselling protection
- [ ] Pagination and sorting (price, newest)
- [ ] Mobile Money payments (MTN / Airtel via Flutterwave or Pesapal)
- [ ] Email notifications for new orders
- [ ] Deployment with PostgreSQL and cloud media storage

## Notes

- This project is in development. Set `DEBUG = False`, use a new `SECRET_KEY` from environment variables, and configure `ALLOWED_HOSTS` before deploying.
- Uploaded images in `media/` and the local `db.sqlite3` should not be committed (see `.gitignore`).

## License

This project was developed for educational and demonstration purposes. A formal open-source license can be added if the project is intended for public reuse.
