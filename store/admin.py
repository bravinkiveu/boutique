from django.contrib import admin
from .models import Coupon, ProductImage, Address


# Admin Site Branding
admin.site.site_header = 'Bravin Boutique'
admin.site.site_title = 'Bravin Boutique Admin'
admin.site.index_title = 'Store Management'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active')
    list_filter = ('active',)
    search_fields = ('code',)
    list_editable = ('active',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_filter = ('product',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'county', 'town', 'is_default', 'created_at')
    list_filter = ('county', 'is_default')
    search_fields = ('full_name', 'phone', 'town')
