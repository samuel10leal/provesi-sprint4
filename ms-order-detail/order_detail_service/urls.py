from django.urls import path
from api import views

urlpatterns = [
    path("orders/<int:order_id>/full", views.order_full_detail, name="order_full_detail"),
]
