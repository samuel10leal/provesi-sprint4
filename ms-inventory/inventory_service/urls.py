from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("inventory", views.inventory_list, name="inventory_list"),
]
