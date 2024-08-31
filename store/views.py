from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem

def home(request):
    featured_products = Product.objects.all()[:4]  # Get 4 featured products
    return render(request, 'store/home.html', {'featured_products': featured_products})

def product_catalog(request):
    products = Product.objects.all()
    return render(request, 'store/product_catalog.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def cart(request):
    # For now, we'll use a simple session-based cart
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        total += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'checkout_url': '/checkout/'  # Add a URL for the checkout page
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        print(f"Session: {request.session.items()}")
        print(f"Cart Product ID: {cart.get(product_id, 0)}")
        product_id_str = str(product_id)
        cart[product_id_str] = cart.get(product_id_str, 0) + quantity
        request.session['cart'] = cart
        messages.success(request, f'{product.name} added to cart.')
        print(f"Product ID: {product_id}")
        print(f"Quantity: {quantity}")
        print(f"Cart: {request.session['cart']}")
    return redirect('product_detail', product_id=product_id)

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save()
            cart = request.session.get('cart', {})
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
            request.session['cart'] = {}  # Clear the cart
            return redirect('order_success')
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'form': form})

def order_success(request):
    return render(request, 'store/order_success.html')