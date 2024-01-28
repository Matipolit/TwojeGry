from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import path, include


def logout_view(request):
    logout(request)
    return redirect("/login")


urlpatterns = [
    path('', include("TwojeGryApp.urls")),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html",next_page=("/")), name='login'),
    path("logout/", logout_view, name="logout"),
]
