from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoomOrderSerializer
from rest_framework.permissions import IsAuthenticated

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
        data = request.data
        data['user'] = request.user.id
        serializer = RoomOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
