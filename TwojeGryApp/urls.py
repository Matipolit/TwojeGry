from django.urls import path, register_converter

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manage_copies/", views.manage_copies_list_games, name="manage_copies"),
    path("manage_copies/<int:game_id>", views.manage_copies, name="manage_copies"),
    path("manage_copies/create/<int:game_id>", views.manage_copies_create, name="manage_copies"),
    path("manage_copies/edit/<int:copy_id>", views.manage_copies_edit, name="manage_copies"),
    path("manage_copies/delete/<int:copy_id>", views.manage_copies_delete, name="manage_copies"),
    path("manage_rentals/", views.manage_rentals, name="manage_rentals"),
]
