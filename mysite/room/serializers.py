from rest_framework import serializers

from .models import RoomOrder, StaffListOrder

class RoomOrderSerializer(serializers.ModelSerializer):
    # start_time = serializers.DateTimeField()
    class Meta:
        model = RoomOrder
        fields = ['room_name', 'start_time', 'end_time']

class StaffListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffListOrder
        fields = ['id_RoomOrder', 'staff_email', 'staff_full_name']