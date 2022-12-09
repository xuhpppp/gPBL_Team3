from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status

from room.models import StaffOrder
from room.serializers import StaffOrderSerializer

import sys

sys.path.append("..")

# Create your views here.
class CheckIn(APIView):
    def post(self, request):
        result = ''
        complete = 0

        list_of_online_users = request.data.get('online_users')
        for name in list_of_online_users:
            if name != 'unknown':
                user_id = int(name.split('-')[1])
                
                staff_order = StaffOrder.objects.all().filter(roomOrder_id=request.data['roomOrder_id']).filter(user_id=user_id)
                if (len(staff_order) > 0):
                    mutable_data = {}
                    mutable_data['roomOrder'] = request.data['roomOrder_id']
                    mutable_data['user'] = user_id
                    mutable_data['joined'] = True

                    serializer = StaffOrderSerializer(staff_order[0], mutable_data)

                    if serializer.is_valid():
                        serializer.save()
                        complete = 1

                        result += name.split('-')[0] + ', '
                    else:
                        return JsonResponse({
                            'message': 'Something wrong!'
                        }, status = status.HTTP_400_BAD_REQUEST)

        if complete == 1:
            return JsonResponse({
                'message': 'Check-in completely for ' + result[:len(result) - 2]
            }, status = status.HTTP_200_OK)
        else:
            return JsonResponse({
                'message': 'Scan complete, there is no change'
            }, status = status.HTTP_200_OK)