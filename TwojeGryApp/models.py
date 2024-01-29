from django.db import models
from django_enumfield import enum
from datetime import datetime


class Genre(enum.Enum):
    Euro = 1
    Ameritrash = 2
    ForKids = 3
    Family = 4
    Party = 5
    Economical = 6
    Strategic = 7
    Cooperative = 8
    War = 9
    Battle = 10
    Hybrid = 11
    Card = 12


class Game(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    genre = enum.EnumField(Genre, default=Genre.Card, null=False, blank=False)
    min_players = models.IntegerField(null=False, blank=False)
    max_players = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class Client(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    surname = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return f"{self.name} {self.surname}"


class GameCopy(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=False, blank=False)
    time_bought = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"{self.game_id.name} {self.time_bought}"


class Order(models.Model):
    game_copy_id = models.ForeignKey(GameCopy, on_delete=models.CASCADE, null=False, blank=False)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)
    date_ordered = models.DateField(null=False, blank=False)
    date_returned = models.DateField(null=True, blank=True)

    @property
    def is_now(self):
        return self.date_returned > datetime.now().date() > self.date_ordered

    def price(self, pricing):
        if (self.date_returned == None):
            return pricing.price_per_day * (self.date_ordered - datetime.now().date()).days
        else:
            return pricing.price_per_day * (self.date_returned - self.date_ordered).days


class Pricing(models.Model):
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    price_per_delayed_day = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
