from django.db import models

# Create your models here.
class RoomOrder(models.Model):
    room_name: models.CharField(max_length=255)
    orderer_email: models.EmailField(max_length=255)
    orderer_full_name: models.CharField(max_length=255)
    start_time: models.DateTimeField()
    end_time: models.DateTimeField()

class StaffListOrder(models.Model):
    id_RoomOrder: models.PositiveIntegerField()
    staff_email: models.CharField(max_length=255)
    staff_full_name: models.CharField(max_length=255)