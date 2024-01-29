from django.test import TestCase
from .models import *
from datetime import timezone, datetime, timedelta, date

class OrderTestCase(TestCase):
    monopoly = None
    monopolyCopy = None
    client = None
    order = None
    pricing = None

    def setUp(self):
        self.monopoly = Game.objects.create(name = "Monopoly", min_players = 2,max_players = 4, price = 124.99)
        self.monopolyCopy = GameCopy.objects.create(game_id =self.monopoly, time_bought = datetime.now().date()) 
        self.client = Client.objects.create(name= "Wacław", surname = "Zientarski", email = "wacław@gmail.com", phone_number= "123456789")
        delta = timedelta(days=4)
        self.order = Order.objects.create(game_copy_id =self.monopolyCopy, client_id=self.client, date_ordered= datetime.now().date() - delta, date_returned= datetime.now().date() + delta)
        self.pricing = Pricing.objects.create(price_per_day=3, price_per_delayed_day= 6)

    def test_order_is_now(self):
        self.assertTrue(self.order.is_now)

    def test_order_price(self):
        self.assertEquals(self.order.price(pricing = self.pricing), 24)
    
