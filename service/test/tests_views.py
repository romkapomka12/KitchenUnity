# from django.conf import settings settings.configure()
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from service.models import DishType, Dish, Cook, Ingredient

DISH_TYPES_URL = reverse("service:dish_type_list")
DISH_URL = reverse("service:dish_list")
INGREDIENT_URL = reverse("service:dish_ingredient_list")


class PublicIngredientListTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(INGREDIENT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientListtest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_login(self.user)
        self.dish = Dish.objects.create(name="Sample Dish")
        self.dish_type = DishType.objects.create(name='Salad')
        self.cook = Cook.objects.create_user(username='cookuser', password='cookpass', position='SH')
        self.ingredient1 = Ingredient.objects.create(name='Lettuce', unit='g', quantity=200, dish=self.dish)
        self.ingredient2 = Ingredient.objects.create(name='Croutons', unit='g', quantity=50, dish=self.dish)

    def test_ingredient_list_view(self):
        dish = Dish.objects.create(name="Sample Dish")
        dish_type = DishType.objects.create(name='Salad')
        ingredient1 = Ingredient.objects.create(name='Lettuce', unit='g', quantity=200, dish=dish)
        ingredient2 = Ingredient.objects.create(name='Croutons', unit='g', quantity=50, dish=dish)

        response = self.client.get(reverse('service:ingredient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/dish_ingredient_list.html')
        self.assertContains(response, ingredient1.name)
        self.assertContains(response, ingredient2.name)

    def test_login_required(self):
        res = self.client.get('service:dish_ingredient_list', kwargs={'pk': self.dish.pk})

        self.assertNotEqual(res.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        # Перевіряємо, чи URL відображається правильно
        url = reverse('service:dish_ingredient_list', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Перевіряємо, чи використовується правильний шаблон для відображення
        url = reverse('service:dish_ingredient_list', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'service/dish_ingredient_list.html')

    def test_view_returns_correct_context(self):
        # Перевіряємо, чи повертається правильний контекст даних
        url = reverse('service:dish_ingredient_list', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.context['object'], self.dish)
        self.assertQuerysetEqual(response.context['dish_ingredient_list'],
                                 [repr(self.ingredient1), repr(self.ingredient2)], ordered=False)



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


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook1234",
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "admin",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "year_of_experience": 5,
            "position": "Sous Chef",
        }
        response = self.client.post(reverse("service:cook_create"), data=form_data)
        self.assertEqual(response.status_code, 200)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position, form_data["position"])
        self.assertEqual(new_user.year_of_experience, form_data["year_of_experience"])









