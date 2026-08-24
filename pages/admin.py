from django.contrib import admin

from .models import (
    Coffee,
    Order,
    OrderItem,
    Feedback
)


# ==========================================
# COFFEE ADMIN
# ==========================================

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'is_available',
    )

    list_filter = (
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )

    list_editable = (
        'price',
        'is_available',
    )


# ==========================================
# ORDER ITEM INLINE
# ==========================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0
    fields = (
        'coffee',
        'quantity',
        'price',
        'subtotal',
    )

    readonly_fields = (
        'price',
        'subtotal',
    )


# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'phone',
        'coffee_items',
        'pickup_time',
        'total_price',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'instructions',
        'items__coffee__name',
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
        'total_price',
    )

    ordering = (
        '-created_at',
    )

    inlines = (
        OrderItemInline,
    )

    def coffee_items(self, obj):
        items = obj.items.all()
        return ", ".join(
            f"{item.coffee.name} × {item.quantity}"
            for item in items
        )
    coffee_items.short_description = 'COFFEE / QUANTITY'


# ==========================================
# FEEDBACK ADMIN
# ==========================================

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'message',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )