from django.test import TestCase

from service.forms import (DishSearchForm,
                           CooksCreationForm,
                           CooksSearchForm,
                           )


class CooksCreationFormTests(TestCase):
    def test_cook_create_with_position_lastname_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "position": "PG",
        }
        form = CooksCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DishSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_name"}
        form = DishSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class CooksSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "username"
        form_data = {field: "test_name"}
        form = CooksSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
