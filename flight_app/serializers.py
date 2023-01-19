from rest_framework import serializers
from .models import *


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"
        extra_kwargs = {"first_name": {"required": False},
                        "last_name": {"required": False}, }


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only=True)
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField(read_only=True)
    passenger = PassengerSerializer(many=True, required=False)

    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user_id'] = self.context.get('request').user.id
        passenger_data = validated_data.pop("passenger")
        reservation = Reservation.objects.create(**validated_data)

        for passenger in passenger_data:
            id = passenger.get("id")
            print("id", passenger, passenger.validated_data)
            if id:
                new_passenger = Passenger.objects.get(id=id)
            else:
                new_passenger = Passenger.objects.create(**passenger)
            reservation.passenger.add(new_passenger)

        reservation.save()
        return reservation


class StaffFlightSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "flight_number", "airlines", "departure_city",
                  "arrival_city", "date", "time", "reservation")
