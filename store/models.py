from django.db import models
from django.contrib.auth.models import User


class Coupon(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount = models.PositiveIntegerField(
        help_text="Percentage discount"
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.code


class ProductImage(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(
        upload_to='gallery/'
    )

    def __str__(self):
        return self.product.name


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

    address = models.TextField()

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.town}"

