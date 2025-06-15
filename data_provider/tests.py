from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from data_provider.models import Event
from django.utils.timezone import now
import json

class EventTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            hotel_id=1,
            original_event_id=123,
            timestamp=now(),
            rpg_status=1,
            room_id="101",
            night_of_stay=now().date()
        )

    def test_get_events(self):
        url = reverse('event-list-create')
        response = self.client.get(url, {'hotel_id': 1}, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_create_event(self):
        url = reverse('event-list-create')
        data = {
            "hotel_id": 1,
            "original_event_id": 456,
            "timestamp": now().isoformat(),
            "rpg_status": 1,
            "room_id": "102",
            "night_of_stay": now().date().isoformat()
        }
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 2)

