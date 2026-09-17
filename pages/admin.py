from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Coffee,
    Order,
    OrderItem,
    Feedback
)


# ==========================================
# SITE BRANDING
# ==========================================

admin.site.site_header = "Hanni's Coffee Shop"
admin.site.site_title = "Hanni's Admin"
admin.site.index_title = "Dashboard"


# ==========================================
# HELPERS
# ==========================================

def pill(text, kind='info'):
    """Chhota sa colored badge (CSS admin-theme.css me hai)."""
    return format_html(
        '<span class="hanni-pill hanni-pill--{}">{}</span>',
        kind,
        text
    )


def money(value):
    amount = f"{value:,.2f}"
    if amount.endswith('.00'):
        amount = amount[:-3]
    return format_html(
        '<span class="hanni-money">Rs {}</span>',
        amount
    )


# ==========================================
# COFFEE ADMIN
# ==========================================

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):

    list_display = (
        'thumbnail',
        'name',
        'availability',
        'price',
    )

    list_display_links = (
        'thumbnail',
        'name',
    )

    list_editable = (
        'price',
    )

    actions = (
        'mark_available',
        'mark_unavailable',
    )

    list_filter = (
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = (
        'name',
    )

    list_per_page = 25

    readonly_fields = (
        'image_preview',
    )

    fieldsets = (
        ('Coffee details', {
            'fields': (
                'name',
                'description',
            ),
        }),
        ('Pricing and availability', {
            'fields': (
                'price',
                'is_available',
            ),
        }),
        ('Image', {
            'fields': (
                'image',
                'image_preview',
            ),
        }),
    )

    @admin.display(description='')
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="hanni-thumb" alt="">',
                obj.image.url
            )
        return format_html(
            '<span class="hanni-muted">No image</span>'
        )

    @admin.display(description='Status', ordering='is_available')
    def availability(self, obj):
        if obj.is_available:
            return pill('In stock', 'ok')
        return pill('Unavailable', 'off')

    @admin.action(description='Mark selected coffees as available')
    def mark_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(
            request,
            f"{updated} coffee(s) ab available hain."
        )

    @admin.action(description='Mark selected coffees as unavailable')
    def mark_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(
            request,
            f"{updated} coffee(s) ab unavailable hain."
        )

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:220px;border-radius:10px;">',
                obj.image.url
            )
        return format_html(
            '<span class="hanni-muted">Koi image upload nahi hui.</span>'
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
        'subtotal_display',
    )

    readonly_fields = (
        'subtotal_display',
    )

    verbose_name = 'Order item'
    verbose_name_plural = 'Order items'

    @admin.display(description='Subtotal')
    def subtotal_display(self, obj):
        if obj.pk:
            return money(obj.subtotal)
        return '-'


# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_ref',
        'name',
        'phone',
        'coffee_items',
        'pickup',
        'total_display',
        'placed_on',
    )

    list_display_links = (
        'order_ref',
        'name',
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

    date_hierarchy = 'created_at'

    readonly_fields = (
        'created_at',
        'total_display',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    inlines = (
        OrderItemInline,
    )

    fieldsets = (
        ('Customer', {
            'fields': (
                'name',
                'phone',
            ),
        }),
        ('Pickup', {
            'fields': (
                'pickup_time',
                'instructions',
            ),
        }),
        ('Summary', {
            'fields': (
                'total_display',
                'created_at',
            ),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('items__coffee')

    @admin.display(description='Order', ordering='id')
    def order_ref(self, obj):
        return format_html(
            '<span class="hanni-money">{}</span>',
            f"#{obj.id:04d}"
        )

    @admin.display(description='Items')
    def coffee_items(self, obj):
        items = obj.items.all()
        if not items:
            return format_html(
                '<span class="hanni-muted">No items</span>'
            )
        text = ", ".join(
            f"{item.coffee.name} x {item.quantity}"
            for item in items
        )
        return format_html(
            '<span class="hanni-items">{}</span>',
            text
        )

    @admin.display(description='Pickup', ordering='pickup_time')
    def pickup(self, obj):
        if not obj.pickup_time:
            return format_html(
                '<span class="hanni-muted">-</span>'
            )
        return pill(
            obj.pickup_time.strftime('%I:%M %p'),
            'info'
        )

    @admin.display(description='Total')
    def total_display(self, obj):
        return money(obj.total_price)

    @admin.display(description='Placed on', ordering='created_at')
    def placed_on(self, obj):
        return format_html(
            '<span class="hanni-muted">{}</span>',
            obj.created_at.strftime('%d %b %Y, %I:%M %p')
        )


# ==========================================
# FEEDBACK ADMIN
# ==========================================

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'rating_display',
        'message_preview',
        'received_on',
    )

    list_display_links = (
        'name',
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

    date_hierarchy = 'created_at'

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    fieldsets = (
        ('Customer', {
            'fields': (
                'name',
                'email',
            ),
        }),
        ('Feedback', {
            'fields': (
                'rating',
                'message',
                'created_at',
            ),
        }),
    )

    POSITIVE = ('excellent', 'great', 'good', 'amazing', 'love', '5', '4')
    NEGATIVE = ('bad', 'poor', 'worst', 'terrible', 'awful', '1', '2')

    @admin.display(description='Rating', ordering='rating')
    def rating_display(self, obj):
        value = (obj.rating or '').strip()
        lowered = value.lower()

        if any(word in lowered for word in self.POSITIVE):
            kind = 'ok'
        elif any(word in lowered for word in self.NEGATIVE):
            kind = 'off'
        else:
            kind = 'info'

        return pill(value or 'Not rated', kind)

    @admin.display(description='Message')
    def message_preview(self, obj):
        text = obj.message or ''
        if len(text) > 70:
            text = text[:70].rstrip() + '...'
        return format_html(
            '<span class="hanni-items">{}</span>',
            text
        )

    @admin.display(description='Received on', ordering='created_at')
    def received_on(self, obj):
        return format_html(
            '<span class="hanni-muted">{}</span>',
            obj.created_at.strftime('%d %b %Y, %I:%M %p')
        )
