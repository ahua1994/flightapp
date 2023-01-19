from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Flight(models.Model):
    flight_number = models.CharField(max_length=8)
    airlines = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=20)
    arrival_city = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.date} -- {self.airlines} - {self.departure_city} to {self.arrival_city}"

    class Meta:
        ordering = ["date"]


class Passenger(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} - {self.first_name}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True)
    passenger = models.ManyToManyField(Passenger)

    def __str__(self):
        return f"{self.flight} {self.user.username}"
