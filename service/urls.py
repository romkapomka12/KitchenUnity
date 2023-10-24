
from django.urls import path

from service import views
from service.views import (
    index,
    DishTypesListView,
    CookListView,
    DishListView,
    DishDetailView,
    CooksCreateView,
    DishCreateView,
    DishTypesCreateView,
    DishUpdateView,
    DishDeleteView,
    CooksUpdateView,
    CooksDeleteView,
    DishTypesUpdateView,
    DishTypesDeleteView,
    CooksDetailView,
    IngredientListView,
    IngredientUpdateView,
    IngredientDeleteView,
    IngredientCreateView,

)

urlpatterns = [
    path("", index, name="index"),
    path("dish_types/", DishTypesListView.as_view(), name="dish_type_list"),
    path("dish_types/create/", DishTypesCreateView.as_view(), name="dish_type_create"),
    path("dish_types/<int:pk>/update/", DishTypesUpdateView.as_view(), name="dish_type_update"),
    path("dish_types/<int:pk>/delete/", DishTypesDeleteView.as_view(), name="dish_type_delete"),
    path("cooks/", CookListView.as_view(), name="cook_list"),
    path("cooks/create/", CooksCreateView.as_view(), name="cook_create"),
    path("cooks/<int:pk>/", CooksDetailView.as_view(), name="cook_detail"),
    path("cooks/<int:pk>/update/", CooksUpdateView.as_view(), name="cook_update"),
    path("cooks/<int:pk>/delete/", CooksDeleteView.as_view(), name="cook_delete"),
    path("dishs/", DishListView.as_view(), name="dish_list"),
    path("dishs/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dishs/<int:pk>/update/", DishUpdateView.as_view(), name="dish_update"),
    path("dishs/<int:pk>/delete/", DishDeleteView.as_view(), name="dish_delete"),
    path("dishs/create/", DishCreateView.as_view(), name="dish_create"),
    path("dishs/<int:pk>/update/ingredient/", IngredientListView.as_view(), name="dish_ingredient_list"),
    path("dishs/<int:pk>/update/ingredient/create/", IngredientCreateView.as_view(), name="dish_ingredient_create"),
    path("dishs/<int:dish_pk>/update/ingredient/<int:pk>/update/", IngredientUpdateView.as_view(), name="dish_ingredient_update"),
    path("dishs/<int:dish_pk>/update/ingredient/<int:pk>/delete/", IngredientDeleteView.as_view(), name="dish_ingredient_delete"),

]

app_name = "service"
