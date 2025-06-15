import csv
from django.core.management.base import BaseCommand
from data_provider.models import Event
from django.utils.dateparse import parse_datetime, parse_date
from datetime import datetime, timezone
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Load events from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            print(reader.fieldnames)  # Debugging line to check field names
        
            count = 0
            for row in reader:
                 # Parse event_timestamp: '24-06-2022 13:00'
                parsed_dt = datetime.strptime(row['event_timestamp'], '%Y-%m-%d %H:%M:%S')
                aware_dt = make_aware(parsed_dt, timezone.utc)

                # Parse night_of_stay: '26-06-2022'
                night_stay = datetime.strptime(row['night_of_stay'], '%Y-%m-%d').date()


                Event.objects.create(
                    hotel_id=int(row['hotel_id']),
                    original_event_id=int(row['id']),
                    timestamp=aware_dt,
                    rpg_status=int(row['status']),
                    room_id=row['room_reservation_id'],
                    night_of_stay=night_stay,
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} events'))
