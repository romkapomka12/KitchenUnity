from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from service.models import Cook, Dish, Ingredient


class CooksCreationForm(UserCreationForm):

    class Meta(
        UserCreationForm.Meta
    ):
        model = Cook
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position",)


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CooksSearchForm(forms.Form):
    username = forms.CharField(
        # max_lenght=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."}))


class DishSearchForm(forms.Form):
    name = forms.CharField(
        # max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."}))
