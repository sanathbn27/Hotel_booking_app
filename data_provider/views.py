from django.shortcuts import render

from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('timestamp')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'hotel_id': ['exact'],
        'rpg_status': ['exact'],
        'room_id': ['exact'],
        'night_of_stay': ['gte', 'lte'],
        'timestamp': ['gte', 'lte'],
    }
    ordering_fields = ['timestamp']
