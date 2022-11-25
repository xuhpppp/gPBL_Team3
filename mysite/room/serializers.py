from rest_framework import serializers

from .models import RoomOrder, StaffOrder

class RoomOrderSerializer(serializers.ModelSerializer):
    # start_time = serializers.DateTimeField()
    class Meta:
        model = RoomOrder
        fields = ['user', 'room_name', 'start_time', 'end_time', 'id']

class StaffOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffOrder
        fields = ['roomOrder_id', 'user_id', 'joined']