from datetime import datetime,timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoomOrderSerializer, StaffOrderSerializer
from rest_framework.permissions import IsAuthenticated

from .models import RoomOrder, StaffOrder
from authen.models import User

# Create your views here.
class OrderTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk == None:
            if request.user.is_admin:
                data = RoomOrder.objects.filter(
                    start_time__gte=str(datetime.now()))
            else:
                data = RoomOrder.objects.filter(user_id=request.user.id).filter(
                    start_time__gte=str(datetime.now()))
        else:
            try:
                if request.user.is_admin:
                    data = RoomOrder.objects.filter(pk=pk).filter(
                        start_time__gte=str(datetime.now()))
                else:
                    data = RoomOrder.objects.filter(
                        user_id=request.user.id).filter(pk=pk).filter(
                        start_time__gte=str(datetime.now()))
            except:
                return Response({'message': 'No valid records found'})

        serializer = RoomOrderSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        start_time = datetime.strptime(
            request.data['start_time'], '%Y/%m/%d %H:%M')
        end_time = datetime.strptime(
            request.data['end_time'], '%Y/%m/%d %H:%M')
        print('>>>>>> start time: ',start_time)
        if start_time > end_time or start_time < datetime.now():
            return Response({'message': 'Input time invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if start_time < (datetime.now() + timedelta(minutes=15)):
            return Response({"message": 'Enter time 15 minutes from now'}, status=status.HTTP_400_BAD_REQUEST)
        data['user_id'] = request.user.id
        data['start_time'] = start_time
        data['end_time'] = end_time
        serializer = RoomOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)

        return Response({'message': 'Record creation successful'}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        if request.user.is_admin:
            return Response({'message': 'Permission not granted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if RoomOrder.objects.filter(pk=pk).filter(user_id=request.user.id).count() <= 0:
                return Response({'message': 'Objects do not exist'}, status=status.HTTP_400_BAD_REQUEST)

            room_order = RoomOrder.objects.filter(
                pk=pk).filter(user_id=request.user.id)
            data = request.data

            serializer = RoomOrderSerializer(room_order[0], data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Object updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if request.user.is_admin:
            return Response({'message': 'Permission not granted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if RoomOrder.objects.filter(pk=pk).filter(user_id=request.user.id).count() <= 0:
                return Response({'message': 'Objects do not exist'}, status=status.HTTP_400_BAD_REQUEST)

            room_order = RoomOrder.objects.filter(
                pk=pk).filter(user_id=request.user.id)[0]
            data = request.data

            room_order.delete()

            return Response({'message': 'Object deleted successfully'}, status=status.HTTP_200_OK)

class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    # render list
    def get(self, request):
        my_orders = RoomOrder.objects.all().select_related()
        my_orders_user = []
        is_host = []
        for o in my_orders:
            my_orders_user.append(o.user.full_name)

            if (request.user.id == o.user.id):
                is_host.append(1)
            else:
                is_host.append(0)

        serializer = RoomOrderSerializer(my_orders, many=True)

        return JsonResponse({
           'order_list': serializer.data,
           'order_list_user': my_orders_user,
           'is_host': is_host
        }, status = status.HTTP_200_OK)

    # filter
    def post(self, request):
        my_orders = RoomOrder.objects.all().select_related()
        filter_order = []
        my_orders_user = []
        is_host = []

        serializer = RoomOrderSerializer(my_orders, many=True)

        if request.data['end_time'] == '':
            start = datetime.strptime(request.data['start_time'], "%Y-%m-%d %H:%M")
            
            for i in range(0, len(my_orders)):
                model_temp = dict(serializer.data[i])
                model_start_time = datetime.strptime(model_temp['start_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

                if start <= model_start_time:
                    filter_order.append(my_orders[i])
                    my_orders_user.append(my_orders[i].user.full_name)
                    if request.user.id == my_orders[i].user.id:
                        is_host.append(1)
                    else:
                        is_host.append(0)
            
            serializer_tosend = RoomOrderSerializer(filter_order, many=True)

            return JsonResponse({
                'filter_order': serializer_tosend.data,
                'order_list_user': my_orders_user,
                'is_host': is_host
            }, status = status.HTTP_200_OK)

        if request.data['start_time'] == '':
            end = datetime.strptime(request.data['end_time'], "%Y-%m-%d %H:%M")

            for i in range(0, len(my_orders)):
                model_temp = dict(serializer.data[i])
                model_end_time = datetime.strptime(model_temp['end_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

                if end >= model_end_time:
                    filter_order.append(my_orders[i])
                    my_orders_user.append(my_orders[i].user.full_name)
                    if request.user.id == my_orders[i].user.id:
                        is_host.append(1)
                    else:
                        is_host.append(0)
            
            serializer_tosend = RoomOrderSerializer(filter_order, many=True)

            return JsonResponse({
                'filter_order': serializer_tosend.data,
                'order_list_user': my_orders_user,
                'is_host': is_host
            }, status = status.HTTP_200_OK)

        start = datetime.strptime(request.data['start_time'], "%Y-%m-%d %H:%M")
        end = datetime.strptime(request.data['end_time'], "%Y-%m-%d %H:%M")

        for i in range(0, len(my_orders)):
            model_temp = dict(serializer.data[i])
            model_start_time = datetime.strptime(model_temp['start_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')
            model_end_time = datetime.strptime(model_temp['end_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

            if start <= model_start_time and end >= model_end_time:
                filter_order.append(my_orders[i])
                my_orders_user.append(my_orders[i].user.full_name)
                if request.user.id == my_orders[i].user.id:
                    is_host.append(1)
                else:
                    is_host.append(0)
            
        serializer_tosend = RoomOrderSerializer(filter_order, many=True)

        return JsonResponse({
            'filter_order': serializer_tosend.data,
            'order_list_user': my_orders_user,
            'is_host': is_host
        }, status = status.HTTP_200_OK)

class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        room_order = get_object_or_404(RoomOrder, id=kwargs.get('pk'))

        if room_order is not None:
            serializer = RoomOrderSerializer(room_order, many=False)

            return JsonResponse({
                'room_order': serializer.data
            }, status = status.HTTP_200_OK)

class StaffList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        staff_list = StaffOrder.objects.all().filter(roomOrder=kwargs.get('pk')).select_related()
        serializer = StaffOrderSerializer(staff_list, many=True)

        staff_full_name = []
        for staff in staff_list:
            staff_full_name.append(staff.user.full_name)

        return JsonResponse({
            'staff_list': serializer.data,
            'staff_full_name': staff_full_name
        }, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        room_order = get_object_or_404(RoomOrder, id=kwargs.get("pk"))

        if room_order is not None:
            if request.user.id != room_order.user_id:
                return JsonResponse({
                    'message': "You don't enough hierarchy to do that!"
                }, status = status.HTTP_400_BAD_REQUEST)
            
            staff = get_object_or_404(User, email=request.data['email'])
            
            if staff is not None:
                staff_order = StaffOrder.objects.all().filter(roomOrder_id=kwargs.get("pk")).filter(user_id=staff.id)
                if len(staff_order) > 0:
                    return JsonResponse({
                        'message': 'Already have this guest!'
                    }, status = status.HTTP_400_BAD_REQUEST)
                
                mutable_data = {}
                mutable_data['roomOrder'] = kwargs.get("pk")
                mutable_data['user'] = staff.id
                mutable_data['joined'] = False

                serializer = StaffOrderSerializer(data=mutable_data)
                if serializer.is_valid():
                    
                    last_serializer = serializer.save()
                    print(1)
                    return JsonResponse({
                        'message': 'Add a guest successfully!',
                        'staff_order': serializer.data,
                        'full_name': staff.full_name
                    }, status = status.HTTP_200_OK)
                else:
                    return JsonResponse({
                        'message': 'Something wrong!'
                    }, status = status.HTTP_400_BAD_REQUEST)