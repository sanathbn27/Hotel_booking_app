from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from data_provider.models import Event
from django.utils.timezone import now

class DashboardTestCase(TestCase):
    def setUp(self):
        self.year = now().year
        Event.objects.create(
            hotel_id=1,
            original_event_id=789,
            timestamp=now(),
            rpg_status=1,
            room_id="201",
            night_of_stay=now().date()
        )

    def test_dashboard_month(self):
        url = reverse('dashboard')
        response = self.client.get(url, {
            'hotel_id': 1,
            'period': 'month',
            'year': self.year
        }, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_dashboard_day(self):
        url = reverse('dashboard')
        response = self.client.get(url, {
            'hotel_id': 1,
            'period': 'day',
            'year': self.year
        }, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

