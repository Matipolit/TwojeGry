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
    game = Game.objects.get(id=game_id)
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
    context = {"copies": copies, "game_id": game.id, "game_name": game.name}

    return render(request, "manage_copies.html", context)

class CopyForm(forms.ModelForm):
    class Meta:
        model = GameCopy
        fields = ["game_id", "time_bought"]
        labels = {
            "game_id": "Gra",
            "time_bought": "Data zakupu"
        }
@login_required(login_url='login')
def manage_copies_create(request: HttpRequest, game_id: int):
    if request.method == "POST":
        print("Received new create")
        copy_form = CopyForm(request.POST)
        if copy_form.is_valid():
            print("is valid")
            copy_form.save()
        return manage_copies(request, game_id)
    else:
        copy_form = CopyForm(initial={"game_id": game_id})
        context = {"copy_form": copy_form, "game_id": game_id}
        return render(request, "manage_copies_create.html", context)
    

@login_required(login_url='login')
def manage_copies_edit(request: HttpRequest, copy_id: int):
    copy = GameCopy.objects.get(id=copy_id)
    if request.method== "POST":
        print("Received new edit")
        copy_form = CopyForm(request.POST, instance=copy)
        if copy_form.is_valid():
            print("Is valid")
            copy_form.save()
        return manage_copies(request, copy.game_id.id)
    else:
        copy_form = CopyForm(instance=copy)
        context = {"copy_form": copy_form, "copy": copy}
        return render(request, "manage_copies_edit.html", context)

def manage_copies_delete(request: HttpRequest, copy_id: int):
    copy = GameCopy.objects.get(id=copy_id)
    if request.method == "POST":
        copy.delete()
        return manage_copies(request, copy.game_id.id)
    else:
        context = {"copy": copy}
        return render(request, "manage_copies_delete.html", context)

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

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name","surname","email","phone_number"]
        labels = {
            "name": "Imie",
            "surname": "Nazwisko",
            "email": "Adres Email",
            "phone_number": "Numer Telefonu"
        }

@login_required(login_url='login')
def manage_clients(request: HttpRequest):
    clients = Client.objects.all()
    for client in clients:
        print(f"{client.name}: {client.surname}")
    context = {"clients": clients}
    return render(request,"manage_clients.html",context)


@login_required(login_url='login')
def manage_clients_choose_action(request:HttpRequest):
    return render(request,"manage_clients_choose_action.html")


@login_required(login_url='login')
def manage_clients_edit(request: HttpRequest, client_id: int):
    client = Client.objects.get(id=client_id)
    if request.method== "POST":
        print("Received new edit")
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            print("Is valid")
            client_form.save()
        
        return manage_clients(request)
    else:
        client_form = ClientForm(instance=client)
        context = {"client_form": client_form, "client": client}
        return render(request, "manage_clients_edit.html", context)
    

@login_required(login_url='login')
def manage_clients_create(request: HttpRequest):
    if request.method == "POST":
        print("Received new create")
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            print("is valid")
            client_form.save()
        return manage_clients(request)
    else:
        client_form = ClientForm()
        context = {"client_form": client_form}
        return render(request, "manage_clients_create.html", context)
    

def manage_clients_delete(request: HttpRequest, client_id: int):
    client = Client.objects.get(id=client_id)
    if request.method == "POST":
        client.delete()
        return manage_clients(request)
    else:
        context = {"client": client}
        return render(request, "manage_clients_delete.html", context)
    
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["name","genre","min_players","max_players","price"]
        labels = {
            "name": "Nazwa",
            "genre": "Gatunek",
            "min_players": "Minimalna liczba graczy",
            "max_players": "Maksymalna liczba graczy",
            "price": "Cena"
        }

@login_required(login_url='login')
def manage_games(request: HttpRequest):
    games = Game.objects.all()
    for game in games:
        print(f"{game.name}")
    context = {"games": games}
    return render(request,"manage_games.html",context)


@login_required(login_url='login')
def manage_games_choose_action(request:HttpRequest):
    return render(request,"manage_games_choose_action.html")


@login_required(login_url='login')
def manage_games_edit(request: HttpRequest, game_id: int):
    game = Game.objects.get(id=game_id)
    if request.method== "POST":
        print("Received new edit")
        game_form = GameForm(request.POST, instance=game)
        if game_form.is_valid():
            print("Is valid")
            game_form.save()
        
        return manage_games(request)
    else:
        game_form = GameForm(instance=game)
        context = {"game_form": game_form, "game": game}
        return render(request, "manage_games_edit.html", context)
    

@login_required(login_url='login')
def manage_games_create(request: HttpRequest):
    if request.method == "POST":
        print("Received new create")
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            print("is valid")
            game_form.save()
        return manage_games(request)
    else:
        game_form = GameForm()
        context = {"game_form": game_form}
        return render(request, "manage_games_create.html", context)
    

def manage_games_delete(request: HttpRequest, game_id: int):
    game = Game.objects.get(id=game_id)
    if request.method == "POST":
        game.delete()
        return manage_games(request)
    else:
        context = {"game": game}
        return render(request, "manage_games_delete.html", context)