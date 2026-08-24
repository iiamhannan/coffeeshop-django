from django.db import models


# ==========================================
# COFFEE
# ==========================================

class Coffee(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='coffee/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


# ==========================================
# ORDER
# ==========================================

class Order(models.Model):

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    pickup_time = models.TimeField()

    instructions = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

    @property
    def total_price(self):

        return sum(
            item.subtotal
            for item in self.items.all()
        )


# ==========================================
# ORDER ITEM
# ==========================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    coffee = models.ForeignKey(
        Coffee,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    @property
    def subtotal(self):

        return self.price * self.quantity

    def __str__(self):

        return (
            f"{self.coffee.name} x {self.quantity}"
        )


# ==========================================
# FEEDBACK
# ==========================================

class Feedback(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    rating = models.CharField(
        max_length=30
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} - {self.rating}"