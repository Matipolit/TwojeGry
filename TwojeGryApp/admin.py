from django.contrib import admin
from .models import Game, Client, GameCopy, Order, Pricing


admin.site.register(Game)
admin.site.register(Client)
admin.site.register(GameCopy)
admin.site.register(Order)
admin.site.register(Pricing)