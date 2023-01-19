from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class FlightView(ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["date"]
    filterset_fields = ["airlines", "departure_city", "arrival_city", "date"]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer


class ReservationView(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)
