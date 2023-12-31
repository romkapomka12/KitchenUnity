from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from service.models import DishType, Dish, Cook, Ingredient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

DISH_TYPES_URL = reverse("service:dish_type_list")
DISH_URL = reverse("service:dish_list")
INGREDIENT_URL = reverse("service:dish_ingredient_list", kwargs={"pk": 1})

class PublicIngredientTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(INGREDIENT_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_ingredient(self):
        dish_type = DishType.objects.create(name="test_name")
        dish1 = Dish.objects.create(name="Pizza", price=20.00, dish_type=dish_type)
        dish2 = Dish.objects.create(name="Salad", price=20.00, dish_type=dish_type)
        Ingredient.objects.create(name="Cheese", unit="g", quantity=100, dish=dish1)
        Ingredient.objects.create(name="Tomato", unit="g", quantity=50, dish=dish1)
        Ingredient.objects.create(name="Lettuce", unit="g", quantity=30, dish=dish2)
        Ingredient.objects.create(name="Carrot", unit="g", quantity=20, dish=dish2)

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, 200)

        dish_ingredient2 = Ingredient.objects.filter(dish=dish2)
        dish_ingredient1 = Ingredient.objects.filter(dish=dish1)
        res = self.client.get(reverse("service:dish_ingredient_list", kwargs={"pk": 1}))
        self.assertCountEqual(
            list(res.context["dish_ingredient_list"]),
            list(dish_ingredient1),
        )

        res = self.client.get(reverse("service:dish_ingredient_list", kwargs={"pk": 2}))
        self.assertCountEqual(
            list(res.context["dish_ingredient_list"]),
            list(dish_ingredient2),
        )
        self.assertTemplateUsed(res, "service/dish_ingredient_list.html")


class PublicDishTypesTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DISH_TYPES_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypesTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwertyui"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_types(self):
        DishType.objects.create(name="Braai")
        DishType.objects.create(name="Bread")
        res = self.client.get(DISH_TYPES_URL)
        self.assertEquals(res.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEquals(
            list(res.context["dish_type_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(res, "service/dish_type_list.html")


class PublicDishTest(TestCase):

    def test_login_required(self):
        res = self.client.get(DISH_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwertyui"
        )
        self.client.force_login(self.user)

    def test_retrieve_dish(self):
        dish_type = DishType.objects.create(
            name="test_name",
        )

        dish1 = Dish.objects.create(
            name="Spaghetti Carbonara",
            price=20.00,
            dish_type=dish_type
        )

        dish2 = Dish.objects.create(
            name="Lemon Chicken-Stuffed Pita Pockets",
            description="1. Pour 100-150 g of bacon with small slices from the whole shmatka",
            price=5.99,
            dish_type=dish_type
        )
        dish1.cooks.add(self.user)
        dish2.cooks.add(self.user)

        res = self.client.get(DISH_URL)
        self.assertEquals(res.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEquals(
            list(res.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(res, "service/dish_list.html")


    def test_dish_search(self):
        dish_type = DishType.objects.create(
            name="test_name_1",
        )
        dish_type2 = DishType.objects.create(
            name="test_name_2",
        )
        Dish.objects.create(name="name1", price=20.00, dish_type=dish_type)
        Dish.objects.create(name="name2", price=25.00, dish_type=dish_type2)
        response = self.client.get(DISH_URL, {"name": "test_name_1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(Dish.objects.filter(name="test_name_1"))
        )
