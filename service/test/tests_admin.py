from django.contrib.auth import get_user_model
from django.test import TestCase,  Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123456"
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook1",
            password="password354321",
            year_of_experience=8,
            position="Pastry Chef",
        )

    def test_cook_year_of_experience(self):
        """
        Test whether the year of experience is displayed on the admin page
        """

        url = "http://127.0.0.1:8000/admin/service/cook/"
        res = self.client.get(url)
        self.assertContains(res, self.cook.year_of_experience)

        # url = reverse("admin:service_cook_change",  args=[self.cook.id])
        # response = self.client.get(url)
        # self.assertContains(response, self.cook.year_of_experience)

    def test_cook_in_position(self):
        """
        Test check if the cook's position is on the admin page
        """
        # url = "http://127.0.0.1:8000/admin/service/cook/"
        # res = self.client.get(url)
        # self.assertContains(res, self.cook.position)

        url = reverse("admin:service_cook_change", args=[self.cook.id])
        response = self.client.get(url)
        self.assertContains(response, self.cook.position)

    def test_cook_detail_year_of_experience(self):
        """
        Test whether the year of experience is  on cook detail the admin page
        """
        url = reverse("admin:service_cook_change", args=[self.cook.id])
        response = self.client.get(url)
        self.assertContains(response, self.cook.year_of_experience)
