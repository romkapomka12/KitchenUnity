from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from service.forms import CooksCreationForm, DishForm
from service.models import Dish, Cook, DishType, Ingredient
from .forms import (
    CooksSearchForm,
    DishSearchForm,
)

def index(request: HttpRequest) -> HttpResponse:
    num_dishs = Dish.objects.count()
    num_cooks = Cook.objects.count()
    num_dish_type = DishType.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_dishs": num_dishs,
        "num_cooks": num_cooks,
        "num_dish_type": num_dish_type
    }

    return render(request, "service/index.html", context=context)


class DishTypesListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "service/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 5


class DishTypesCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "service/dish_type_list_form.html"
    success_url = reverse_lazy("service:dish_type_list")
    fields = "__all__"


class DishTypesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "service/dish_type_list_form.html"
    success_url = reverse_lazy("service:dish_type_list")
    fields = "__all__"


class DishTypesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "service/dish_type_list_delete.html"
    success_url = reverse_lazy("service:dish_type_list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "service/dish_ingredient_list.html"
    context_object_name = "dish_ingredient_list"
    paginate_by = 10

    def get_queryset(self):
        dish_pk = self.kwargs.get("pk")
        return Ingredient.objects.filter(dish=dish_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        dish_pk = self.kwargs.get("pk")
        dish = get_object_or_404(Dish, pk=dish_pk)
        context["object"] = dish

        INGREDIENT_URL = reverse("service:dish_ingredient_list", kwargs={'pk': dish_pk})
        context["INGREDIENT_URL"] = INGREDIENT_URL

        return context


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    template_name = "service/dish_ingredient_list_form.html"
    success_url = reverse_lazy("service:dish_ingredient_list")
    fields = ["name", "unit", "quantity"]

    def get_success_url(self):
        dish_pk = self.kwargs.get("dish_pk")
        return reverse("service:dish_ingredient_list", kwargs={"pk": dish_pk})


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    template_name = "service/dish_ingredient_list_form.html"

    fields = ["name", "unit", "quantity"]

    def get_success_url(self):
        dish_pk = self.kwargs.get("pk")
        return reverse("service:dish_ingredient_list", kwargs={"pk": dish_pk})

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        dish_pk = self.kwargs.get("pk")
        dish = get_object_or_404(Dish, pk=dish_pk)
        ingredient.dish = dish
        ingredient.save()
        return HttpResponseRedirect(self.get_success_url())


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "service/dish_ingredient_delete.html"
    success_url = reverse_lazy("service:dish_ingredient_list")

    def get_success_url(self):
        dish_pk = self.kwargs.get("dish_pk")
        return reverse("service:dish_ingredient_list", kwargs={"pk": dish_pk})


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "service/cook_list.html"
    context_object_name = "cook_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_form"] = CooksSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        self.queryset = super(CookListView, self).get_queryset()
        username = self.request.GET.get("username")

        if username:
            return self.queryset.filter(username__icontains=username)
        return self.queryset


class CooksCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = ("first_name", "last_name", "username", "password", "year_of_experience", "position",)
    success_url = reverse_lazy("service:cook_list")
    template_name = "service/cook_list_form.html"


class CooksDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CooksUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ("first_name", "last_name", "username", "password", "year_of_experience", "position",)
    success_url = reverse_lazy("service:cook_list")
    template_name = "service/cook_list_form.html"


class CooksDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "service/cook_list_form_delete.html"
    success_url = reverse_lazy("service:cook_list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "service/dish_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__contains=form.cleaned_data["name"])
        return queryset


class DishDetailView(generic.DetailView):
    model = Dish
    paginate_by = 10


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    success_url = reverse_lazy("service:dish_list")
    template_name = "service/dish_list_form.html"
    form_class = DishForm


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    success_url = reverse_lazy("service:dish_list")
    template_name = "service/dish_list_form.html"
    form_class = DishForm


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "service/dish_list_config_delete.html"
    success_url = reverse_lazy("service:dish_list")




