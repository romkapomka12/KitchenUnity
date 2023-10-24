from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, max_length=8, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    class Meta:
        ordering = ("name",)

    def __str__(self, ):
        return f"{self.name} (cooks: {self.cooks}, dish description:{self.description})"


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    UNIT_CHOICES = [
        ("g", "grams"),
        ("ml", "milliliters"),
        ("th", "Thing"),
        ("te.sp.", "teaspoon"),
        ("tb.sp.", "tablespoon"),
        ("gl", "glass"),
    ]
    unit = models.CharField(max_length=15, choices=UNIT_CHOICES)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="ingredients")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Cook(AbstractUser):
    year_of_experience = models.IntegerField(blank=False, null=True)
    POSITION_CHOICES = [
        ("SH", "Chef"), ("SS", "Sous Chef"),
        ("PG", "Hot Shop Cook"), ("PH", "Cold Shop Cook"),
        ("PK", "Pastry Chef"), ("PZ", "Procurement Chef"),
        ("PL", "Line Cook"), ("ST", "Stuart"),
    ]
    position = models.CharField(max_length=2, blank=False, null=False, choices=POSITION_CHOICES)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"
