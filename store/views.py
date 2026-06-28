from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from shop.models import Product, Order, OrderItem, Review, Wishlist
from .forms import RegisterForm
from django.contrib.auth import login
from .models import Coupon, ProductImage, Address


def home(request):


    products = Product.objects.filter(stock__gt=0)

    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')

    if category:
        products = products.filter(
            category__iexact=category
        )

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    elif sort == 'new':
        products = products.order_by('-id')

    return render(
        request,
        'store/home.html',
        {'products': products}
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    images = ProductImage.objects.filter(product=product)
    
    related_products = Product.objects.filter(
        category=product.category,
        stock__gt=0
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product,
            'reviews': reviews,
            'images': images,
            'related_products': related_products
        }
    )


@login_required
def add_review(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', id=product.id)


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('product_detail', id=id)


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def remove_wishlist(request, id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=id
    ).delete()

    return redirect('wishlist')


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=id)

    item_id = str(id)
    current_quantity = cart.get(item_id, 0)

    if current_quantity < product.stock:
        cart[item_id] = current_quantity + 1

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total,
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart

    return redirect('cart')


def increase_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:
        cart[id] -= 1

        if cart[id] <= 0:
            del cart[id]

    request.session['cart'] = cart

    return redirect('cart')


def checkout(request):

    cart = request.session.get('cart', {})
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * quantity

    discount = 0
    final_total = total

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        coupon_code = request.POST.get('coupon', '')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code,
                    active=True
                )
                discount = coupon.discount
            except Coupon.DoesNotExist:
                discount = 0

        discount_amount = (total * discount) / 100
        final_total = total - discount_amount

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                return render(
                    request,
                    'store/stock_error.html',
                    {'product': product}
                )

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address,
            total_amount=final_total
        )

        html_content = render_to_string(
            'emails/order_confirmation.html',
            {
                'customer_name': customer_name,
                'total': final_total,
                'address': address,
                'phone': phone,
            }
        )

        email_message = EmailMultiAlternatives(
            subject='Bravin Boutique - Order Confirmation',
            body='Thank you for your order.',
            from_email='Bravin Boutique <bravinkiveu@gmail.com>',
            to=[email],
        )

        email_message.attach_alternative(html_content, "text/html")
        # Don't block order placement if email fails (bad credentials, SMTP offline, etc.)
        try:
            email_message.send()
        except Exception:
            # In production you may want to log this exception.
            pass



        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

        request.session['cart'] = {}

        return render(request, 'store/success.html')

    return render(request, 'store/checkout.html', {
        'total': total,
        'discount': discount,
        'final_total': final_total
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/order_history.html',
        {'orders': orders}
    )


@login_required
def dashboard(request):
    # Admin-only dashboard page (mapped to /admin/dashboard/)
    if not (request.user.is_staff or request.user.is_superuser):
        # keep it simple: hide the page from non-admin users
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Forbidden")

    from django.contrib.auth.models import User
    from django.utils import timezone

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0
    total_customers = User.objects.filter(is_staff=False, is_superuser=False).count()

    recent_orders = Order.objects.order_by('-created_at')[:8]
    low_stock_products = Product.objects.filter(stock__lte=5).order_by('stock')[:5]

    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(
        created_at__date=today
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    return render(
        request,
        'dashboard.html',
        {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'recent_orders': recent_orders,
            'low_stock_products': low_stock_products,
            'today_orders': today_orders,
            'today_revenue': today_revenue,
        }
    )




def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def search(request):
    query = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__icontains=query)
    ) if query else Product.objects.none()

    return render(request, 'store/search.html', {
        'products': products,
        'query': query
    })


def clothes(request):
    products = Product.objects.filter(
        category__iexact='clothes'
    )

    return render(request,
                  'store/category.html',
                  {
                      'products': products,
                      'title': 'Clothes'
                  })


def shoes(request):
    products = Product.objects.filter(
        category__iexact='shoes'
    )

    return render(request,
                  'store/category.html',
                  {
                      'products': products,
                      'title': 'Shoes'
                  })


def about(request):
    return render(request, 'store/about.html')


@login_required
def addresses(request):
    addresses = Address.objects.filter(
        user=request.user
    )

    return render(
        request,
        'addresses.html',
        {
            'addresses': addresses
        }
    )


@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            county=request.POST['county'],
            town=request.POST['town'],
            address=request.POST['address']
        )

        return redirect('addresses')

    return render(request, 'add_address.html')

