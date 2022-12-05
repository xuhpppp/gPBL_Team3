from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoomOrderSerializer, StaffOrderSerializer
from rest_framework.permissions import IsAuthenticated

from .models import RoomOrder

# Create your views here.
class OrderTask(APIView):
    permission_classes = [IsAuthenticated]

    # render condition
    def get(self, request):
        # use 'for' loop if number of rooms is large
        room_101_list = list(RoomOrder.objects.all().filter(room_name='101').filter(start_time__lte=datetime.now()).filter(end_time__gte=datetime.now()))
        room_201_list = list(RoomOrder.objects.all().filter(room_name='201').filter(start_time__lte=datetime.now()).filter(end_time__gte=datetime.now()))
        room_301_list = list(RoomOrder.objects.all().filter(room_name='301').filter(start_time__lte=datetime.now()).filter(end_time__gte=datetime.now()))

        room_condition = []
        room_condition.append(len(room_101_list))
        room_condition.append(len(room_201_list))
        room_condition.append(len(room_301_list))

        return JsonResponse({
            'room_condition': room_condition
        }, status = status.HTTP_200_OK)

    # create new order
    def post(self, request):
        mutable_data = {}
        mutable_data['room_name'] = request.data['room_name']
        mutable_data['start_time'] = request.data['start_time']
        mutable_data['end_time'] = request.data['end_time']
        mutable_data['user'] = request.user.id
        
        serializer = RoomOrderSerializer(data=mutable_data)  # type: ignore
        if serializer.is_valid():
            now = datetime.now()
            start = datetime.strptime(mutable_data['start_time'], "%Y-%m-%d %H:%M")
            end = datetime.strptime(mutable_data['end_time'], "%Y-%m-%d %H:%M")

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
            serializer_tocheck = RoomOrderSerializer(list_of_RoomOrder, many=True)
            #filter time here...
            duplicate_flag = 0

            for roomorder in serializer_tocheck.data:
                model_temp = dict(roomorder)
                model_start_time = datetime.strptime(model_temp['start_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')
                model_end_time = datetime.strptime(model_temp['end_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

                if (start >= model_start_time and start <= model_end_time) or (end >= model_start_time and end <= model_end_time) or (start <= model_start_time  and end >= model_end_time):
                    duplicate_flag = 1
                    break

            if duplicate_flag == 1:
                return JsonResponse({
                    'message': 'There is also an order at this time in this room!'
                }, status = status.HTTP_400_BAD_REQUEST)
            else:
                last_save_roomOrder = serializer.save()

                staff_order = {}
                staff_order['user_id'] = request.user.id
                staff_order['roomOrder_id'] = last_save_roomOrder.pk

                staff_order_serializer = StaffOrderSerializer(data=staff_order)
                if staff_order_serializer.is_valid():
                    staff_order_serializer.save()
                
                return JsonResponse({
                    'message': f"Ordered successfully for room {request.data['room_name']} from {request.data['start_time']} to {request.data['end_time']}",
                    'full_name': request.user.full_name,
                    'id': last_save_roomOrder.pk
                }, status = status.HTTP_200_OK)
        else:
            return JsonResponse({
                'message': 'Something wrong!'
            }, status = status.HTTP_400_BAD_REQUEST)
    
    # edit order
    def put(self, request, *args, **kwargs):
        room_order = get_object_or_404(RoomOrder, id=kwargs.get('pk'))

        if room_order is not None:
            serializer_obj = RoomOrderSerializer(room_order, many=False)
            model_temp = dict(serializer_obj.data)
            model_start_time = datetime.strptime(model_temp['start_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

            if request.user.id != room_order.user_id:
                return JsonResponse({
                    'message': "You don't enough hierarchy to do that!"
                }, status = status.HTTP_400_BAD_REQUEST)
            
            if model_start_time <= datetime.now():
                return JsonResponse({
                    'message': "You can only edit the order before it start!"
                }, status = status.HTTP_400_BAD_REQUEST)
            
            mutable_data = {}
            mutable_data['room_name'] = request.data['room_name']
            mutable_data['start_time'] = request.data['start_time']
            mutable_data['end_time'] = request.data['end_time']
            mutable_data['user'] = request.user.id
            serializer = RoomOrderSerializer(room_order, mutable_data)
            if serializer.is_valid():
                now = datetime.now()
                start = datetime.strptime(request.data['start_time'], "%Y-%m-%d %H:%M")
                end = datetime.strptime(request.data['end_time'], "%Y-%m-%d %H:%M")

                if end <= start:
                    return JsonResponse({
                        'message': 'End time must be after start time'
                    }, status = status.HTTP_400_BAD_REQUEST)

                delta = start - now
                if (delta.total_seconds() / 60) < 15:
                    return JsonResponse({
                        'message': 'You must order the room before use 15 minutes'
                    }, status = status.HTTP_400_BAD_REQUEST)

                list_of_RoomOrder = RoomOrder.objects.all().filter(~Q(id=kwargs.get('pk')))
                serializer_tocheck = RoomOrderSerializer(list_of_RoomOrder, many=True)

                #filter time here...
                duplicate_flag = 0

                for roomorder in serializer_tocheck.data:
                    model_temp = dict(roomorder)
                    model_start_time = datetime.strptime(model_temp['start_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')
                    model_end_time = datetime.strptime(model_temp['end_time'][:16].replace('T', ' '), '%Y-%m-%d %H:%M')

                    if (start >= model_start_time and start <= model_end_time) or (end >= model_start_time and end <= model_end_time) or (start <= model_start_time  and end >= model_end_time):
                        duplicate_flag = 1
                        break

                if duplicate_flag == 1:
                    return JsonResponse({
                        'message': 'There is also an order at this time in this room!'
                    }, status = status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                
                    return JsonResponse({
                        'message': f"Change successfully to room {request.data['room_name']} from {request.data['start_time']} to {request.data['end_time']}",
                    }, status = status.HTTP_200_OK)
            else:
                print(serializer.data)
                return JsonResponse({
                    'message': 'Something wrong!'
                }, status = status.HTTP_400_BAD_REQUEST)        

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