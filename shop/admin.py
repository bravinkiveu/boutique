from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Review, Wishlist


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'phone', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'email', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'stock_status_badge')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('price', 'stock')

    @admin.display(description='Status')
    def stock_status_badge(self, obj):
        status = obj.stock_status()
        if status == 'out':
            return '🔴 Out of Stock'
        elif status == 'low':
            return '🟡 Low Stock'
        return '🟢 In Stock'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
