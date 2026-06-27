from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/dashboard/', views.dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('review/<int:id>/', views.add_review, name='add_review'),
    path('wishlist/add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-cart/<int:id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:id>/', views.decrease_cart, name='decrease_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('clothes/', views.clothes, name='clothes'),
    path('shoes/', views.shoes, name='shoes'),
    path('about/', views.about, name='about'),
    path('order-history/', views.order_history, name='order_history'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/add/', views.add_address, name='add_address'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
