from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Page, Product, Kategori, Cart, CartItem, Order, Review

def product_list(request):
    categories = Kategori.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'categories': categories, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price(),
        is_paid=False
    )
    cart.items.all().delete()  # Clear the cart after checkout
    return render(request, 'shop/order_confirmation.html', {'order': order})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")
            comment = request.POST.get('comment', '').strip()
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
        except ValueError:
            return redirect('product_detail', slug=product.slug)
    return redirect('product_detail', slug=product.slug)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, published=True)
    return render(request, 'shop/page_detail.html', {'page': page})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  # Validasi jika hanya admin yang boleh mengakses
        return redirect('product_list')

    # Mengambil statistik untuk admin
    total_products = Product.objects.count()
    total_categories = Kategori.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()

    # Kirim data statistik ke template
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders,
    }
    return render(request, 'shop/admin_dashboard.html', context)
