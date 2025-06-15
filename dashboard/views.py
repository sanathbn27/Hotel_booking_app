from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data_provider.models import Event
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DashboardView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'hotel_id', openapi.IN_QUERY, description="Hotel ID", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'period', openapi.IN_QUERY, description="Period (month or day)", type=openapi.TYPE_STRING, enum=['month', 'day'], required=True
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER, required=True
            ),
        ]
    )
     
    def get(self, request):
        hotel_id = request.GET.get('hotel_id')
        period = request.GET.get('period')
        year = request.GET.get('year')

        if not hotel_id or not period or not year:
            return Response({"error": "hotel_id, period, and year are required parameters."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Convert year to integer
        try:
            year = int(year)
        except ValueError:
            return Response({"error": "year must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter events
        events = Event.objects.filter(
            hotel_id=hotel_id,
            rpg_status=Event.BOOKING,
            timestamp__year=year
        )

        if period == "month":
            data = events.annotate(month=TruncMonth('timestamp')).values('month').annotate(
                bookings=Count('id')).order_by('month')
            result = [{"month": d["month"].strftime("%Y-%m"), "bookings": d["bookings"]} for d in data]

        elif period == "day":
            data = events.annotate(day=TruncDay('timestamp')).values('day').annotate(
                bookings=Count('id')).order_by('day')
            result = [{"day": d["day"].strftime("%Y-%m-%d"), "bookings": d["bookings"]} for d in data]

        else:
            return Response({"error": "Invalid period. Use 'month' or 'day'."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(result)

