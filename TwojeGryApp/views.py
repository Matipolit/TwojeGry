from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Case, When, Value, IntegerField, F, BooleanField, DateField, Max, Min
from django.http import HttpRequest
from django.shortcuts import render
from .models import Game, Client, GameCopy, Order, Pricing
from django.db.models.functions import Concat
from django.db.models import Value, Count
from django import forms
from datetime import datetime
from django.utils import timezone
from time import sleep


def dates_overlap(a_start, a_end, b_start, b_end):
    return (a_start <= b_end) and (b_start <= a_end)


def simulate_payment(result: bool):
    sleep(1)
    return result


@login_required(login_url='login')
def index(request: HttpRequest):
    return render(request, "index.html")


@login_required(login_url='login')
def manage_copies_list_games(request: HttpRequest):
    now = timezone.now()
    games = Game.objects.all().annotate(
        total_copies=Count("gamecopy", distinct=True),
        rented=Count("gamecopy", filter=Q(gamecopy__order__date_returned__gte=now) & Q(gamecopy__order__date_ordered__lte=now)),
        available=F("total_copies") - F("rented")
    ).order_by("name")
    for game in games:
        print(f"{game.name}: {game.rented} rented, {game.available} available")
    print(f"Games: {games}")
    context = {"games": games}
    return render(request, "manage_copies_list_games.html", context)


@login_required(login_url='login')
def manage_copies(request: HttpRequest, game_id: int):
    now = timezone.now()
    copies = GameCopy.objects.filter(game_id=game_id).annotate(
        is_rented=Count("order", filter=Q(order__date_returned__gte=now) & Q(order__date_ordered__lte=now)),
    )
    copies = copies.annotate(
        rental_start=Case(
            When(is_rented__gt=0, then=Min('order__date_ordered')),
            default=None,
            output_field=DateField(),
        ),
        rental_end=Case(
            When(is_rented__gt=0, then=Max('order__date_returned')),
            default=None,
            output_field=DateField(),
        )
    )
    context = {"copies": copies}

    return render(request, "manage_copies.html", context)
@login_required(login_url='login')
def manage_rentals(request: HttpRequest):
    class RentalForm(forms.ModelForm):
        class Meta:
            model = Order
            fields = ['client_id', 'game_copy_id', 'date_ordered', 'date_returned']
            labels = {
                "client_id": "Klient",
                "game_copy_id": "Egzemplarz",
                "date_ordered": "Początek wypożyczenia",
                "date_returned": "Koniec wypożyczenia"
            }
            widgets = {
                "date_ordered": forms.DateInput(attrs={'type': 'date'}),
                "date_returned": forms.DateInput(attrs={'type': 'date'}),
            }

        def clean(self):
            print("cleaning")
            cleaned_data = super().clean()
            date_ordered = cleaned_data.get("date_ordered")
            date_returned = cleaned_data.get("date_returned")
            if date_ordered > date_returned:
                raise forms.ValidationError(
                    "Data zwrotu nie może być wcześniejsza niż data wypożyczenia!"
                )
            # ensure that the game copy is available
            game_copy_id = cleaned_data.get("game_copy_id")
            other_orders = Order.objects.filter(game_copy_id=game_copy_id)
            for order in other_orders:
                if dates_overlap(order.date_ordered, order.date_returned, date_ordered, date_returned):
                    raise forms.ValidationError(
                        f"Egzemplarz jest już wypożyczony w tym czasie ({order.date_ordered} - {order.date_returned}) przez {order.client_id}"
                    )

    rental = RentalForm(request.POST or None)
    errors = rental.errors
    payment = None
    print(f"Errors: {errors}")
    if rental.is_valid():
        payment = simulate_payment(True)
        if payment:
            rental.save()

    context = {
        "rental_form": RentalForm(),
        "errors": errors,
        "payment": payment
    }
    return render(request, "manage_rentals.html", context)
