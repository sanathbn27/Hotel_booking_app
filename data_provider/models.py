from django.db import models


class Event(models.Model):
    BOOKING = 1
    CANCELLATION = 2
    RPG_STATUS_CHOICES = [
        (BOOKING, 'Booking'),
        (CANCELLATION, 'Cancellation'),
    ]
    original_event_id = models.BigIntegerField() 
    hotel_id = models.IntegerField()
    timestamp = models.DateTimeField()
    rpg_status = models.IntegerField(choices=RPG_STATUS_CHOICES)
    room_id = models.CharField(max_length=36)
    night_of_stay = models.DateField()

    def __str__(self):
        return f"Hotel {self.hotel_id}, Room {self.room_id}, {self.get_rpg_status_display()} on {self.night_of_stay}"
