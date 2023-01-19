from faker import Faker
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()
from flight_app.models import Flight
import random
from django.utils import timezone
from datetime import datetime 





airlines = [("Spirit", "NK"), ("Frontier", "F9"),
            ("American", "AA"), ("United", "UA")]
cities = ["New York", "Miami", "Boston",
          "Chicago", "Los Angles", "Dallas", "Denver"]

fake = Faker()


def add_flight():
    flight = Flight()
    number = random.randint(100, 999)
    airline = random.choice(airlines)
    flight.airlines = airline[0]
    flight.flight_number = airline[1] + str(number)
    places = random.sample(cities, 2)
    flight.departure_city = places[0]
    flight.arrival_city = places[1]
    flight.date = fake.date_between(
        start_date=datetime(2023, 1, 1), end_date=datetime(2023, 2, 28))
    flight.time = fake.time()
    flight.save()


    # for post in qs:
    #     post.pud_date_rotation = fake.date_time_between(start_date='-20h', end_date='')
    #     post.save()
for i in range(100):
    add_flight()
