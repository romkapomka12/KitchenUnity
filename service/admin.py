from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from service.models import Dish, DishType, Ingredient, Cook


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):

    def cooks_names(self, obj):
        cooks = obj.cooks.all()
        names = [cook.username for cook in cooks]
        return ", ".join(names)

    list_display = ["name", "dish_type", "description", "cooks_names", "price"]
    list_filter = ["dish_type", "name"]
    search_fields = ["name"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("year_of_experience", "position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("year_of_experience", "position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("first_name", "last_name", "position","year_of_experience",)}),)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "quantity", "unit"]
    list_filter = ["name"]


admin.site.register(DishType)
