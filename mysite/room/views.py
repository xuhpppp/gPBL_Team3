from datetime import datetime, timedelta
import pytz

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoomOrderSerializer
from rest_framework.permissions import IsAuthenticated

from .models import RoomOrder

# - order a room
#     + post method
#     + both admin and staff can order
#     + must order before use 30mins
#     + can't order if there is an order in that room at that time
#     + after order, the StaffListOrder automatically add the orderer to db
#     + can't order if time is in the past
# - edit an order
#     + put method
#     + only admin and the ordered can edit
#     + must edit before use 30mins
#     + can't edit if there is an order in that room at that time
#     + can't edit if the order is the order is done
# - delete an order
#     + delete method
#     + only admin and the ordered can delete
#     + can't edit if the order is the order is done
# - get orders(expand...)
# - StaffListOrder will be developed later

# Create your views here.
class OrderTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        mutable_data = {}
        mutable_data['room_name'] = request.data['room_name']
        mutable_data['start_time'] = request.data['start_time']
        mutable_data['end_time'] = request.data['end_time']
        mutable_data['user'] = request.user.id
        
        serializer = RoomOrderSerializer(data=mutable_data)
        if serializer.is_valid():
            now = datetime.now()
            start = datetime.strptime(mutable_data['start_time'], "%Y-%m-%d %H:%M")
            end = datetime.strptime(mutable_data['end_time'], "%Y-%m-%d %H:%M")
            print(start)
            if end <= start:
                return JsonResponse({
                    'message': 'End time must be after start time'
                }, status = status.HTTP_400_BAD_REQUEST)

            delta = start - now
            if (delta.total_seconds() / 60) < 15:
                return JsonResponse({
                    'message': 'You must order the room before use 15 minutes'
                }, status = status.HTTP_400_BAD_REQUEST)

            list_of_RoomOrder = RoomOrder.objects.all().filter(room_name=mutable_data['room_name']).filter(start_time__gt=datetime.now())
            #filter time here...
            duplicate_flag = 0
            utc=pytz.UTC
            #some bug about UTC timezone
            start = start.replace(tzinfo=utc)
            start = start - timedelta(hours = 7)
            end = end.replace(tzinfo=utc)
            end = end - timedelta(hours = 7)
            #change logic here...
            for roomorder in list_of_RoomOrder:
                if start <= roomorder.end_time:
                    print(start, roomorder.end_time)

            if duplicate_flag == 1:
                return JsonResponse({
                    'message': 'There is also an order at this time in this room!'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            return JsonResponse({
                'message': 'Ordered successfully!'
            }, status = status.HTTP_200_OK)
        else:
            return JsonResponse({
                'message': 'Something wrong!'
            }, status = status.HTTP_400_BAD_REQUEST)
