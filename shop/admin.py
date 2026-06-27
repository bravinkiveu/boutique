from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Review, Wishlist


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'total_amount', 'created_at')
    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'stock'
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
    )


admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)
