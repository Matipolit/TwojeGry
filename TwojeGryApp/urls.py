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
    path("manage_clients/",views.manage_clients, name="manage_clients"),
    path("manage_clients_choose_action/",views.manage_clients_choose_action, name="manage_clients_choose_action"),
    path("manage_clients/edit/<int:client_id>", views.manage_clients_edit, name="manage_clients"),
    path("manage_clients_create/", views.manage_clients_create, name="manage_clients"),
    path("manage_clients/delete/<int:client_id>", views.manage_clients_delete, name="manage_clients"),
    path("manage_games_choose_action/",views.manage_games_choose_action, name="manage_gamets_choose_action"),
    path("manage_games/",views.manage_games, name="manage_games"),
    path("manage_games/edit/<int:game_id>", views.manage_games_edit, name="manage_games"),
    path("manage_games/delete/<int:game_id>", views.manage_games_delete, name="manage_games"),
    path("manage_games_create/", views.manage_games_create, name="manage_games"),
]
