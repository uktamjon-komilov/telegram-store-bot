from django.urls import path
from . import views

urlpatterns = [
    path("bot/", views.main),
    path("", views.stats),
    path("ordered-products/", views.ordered_products, name="ordered-products"),
    path("ordering-regions/", views.ordering_regions, name="ordering-regions"),
    path("types-of-orders/", views.types_of_orders, name="types-of-orders"),
]