from decimal import Decimal
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from main.models import Product
from .forms import OrderForm
from .models import OrderItem


def _cart_details(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    valid_quantities = {}
    for product_id, raw_quantity in cart.items():
        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            continue
        if quantity > 0:
            valid_quantities[str(product_id)] = min(quantity, 99)

    products = Product.objects.filter(id__in=valid_quantities.keys(), available=True)
    items = []
    total_price = Decimal('0.00')
    total_quantity = 0
    for product in products:
        quantity = valid_quantities[str(product.id)]
        line_total = product.price * quantity
        items.append({'product': product, 'quantity': quantity, 'line_total': line_total})
        total_price += line_total
        total_quantity += quantity
    return items, total_price, total_quantity


def cart_detail(request):
    items, total_price, total_quantity = _cart_details(request)
    return render(request, 'main/cart_detail.html', {
        'items': items, 'total_price': total_price, 'total_quantity': total_quantity,
    })


@require_POST
def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id, available=True).first()
    if product:
        cart = request.session.get('cart', {})
        key = str(product.id)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        cart[key] = min(int(cart.get(key, 0)) + max(1, quantity), 99)
        request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, 99)
    request.session['cart'] = cart
    return redirect('cart_detail')


def create_order(request):
    items, total_price, total_quantity = _cart_details(request)
    if not items:
        return redirect('cart_detail')

    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            # Load current prices and availability again when the order is submitted.
            product_ids = [item['product'].id for item in items]
            current_products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(
                    id__in=product_ids, available=True
                )
            }
            if len(current_products) != len(product_ids):
                return redirect('cart_detail')
            order = form.save()
            for item in items:
                product = current_products[item['product'].id]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item['quantity'],
                )
        request.session['cart'] = {}
        return render(request, 'order/order_created.html', {'order': order})

    return render(request, 'order/create_order.html', {
        'form': form, 'items': items, 'total_price': total_price,
        'total_quantity': total_quantity,
    })
