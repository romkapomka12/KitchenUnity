from django.contrib.auth import get_user_model
from django.test import TestCase

from service.models import DishType, Dish, Cook, Ingredient


class ModelTests(TestCase):

    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Biscuits")
        self.assertEquals(str(dish_type), dish_type.name)

    def test_cooks_str(self):
        cooks = get_user_model().objects.create(
            username="Abigail",
            password="qwerty",
            first_name="John",
            last_name="Anderson"
        )
        self.assertEquals(str(cooks), f"{cooks.username}: ({cooks.first_name} {cooks.last_name})")

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Salad")
        cooks = Cook.objects.create(username=["Charles", "Abigail"])
        dish = Dish.objects.create(
            name="Lemon Chicken-Stuffed Pita Pockets",
            price=3.55,
            description="STEP 1 Boil the beets in advance for about an hour until ready...",
            dish_type=dish_type
        )
        dish.cooks.add(cooks)
        self.assertEquals(str(dish), f"{dish.name} (cooks: {dish.cooks}, dish description:{dish.description})")

    def test_create_cooks(self):
        username = "Abigail123"
        password = "qwerty"
        first_name = "Abigail"
        last_name = "Anderson"
        year_of_experience = 8
        position = "SH"
        cooks = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            year_of_experience=year_of_experience,
            position=position
        )
        self.assertEquals(cooks.username, "Abigail123")
        self.assertTrue(cooks.check_password(password))
        self.assertEquals(cooks.first_name, first_name)
        self.assertEquals(cooks.last_name, last_name)
        self.assertEquals(cooks.year_of_experience, year_of_experience)
        self.assertEquals(cooks.position, position)

    def test_ingredient_of_dish(self):
        dish_type = DishType.objects.create(name="Cakes")
        dish = Dish.objects.create(
            name="CHOCOLATE cake",
            price=12.99,
            dish_type=dish_type
        )
        ingredient = Ingredient.objects.create(
            name="chocolate",
            quantity=200.00,
            unit="g",
            dish=dish
        )
        self.assertEquals(str(ingredient), f"{ingredient.name} ({ingredient.quantity} {ingredient.unit})")

