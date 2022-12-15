from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from mysite.settings import BASE_DIR
from datetime import datetime, date, timezone
import os
from room.models import RoomOrder
import json
from rest_framework.permissions import IsAdminUser

FACE_DETECT_PATH = str(BASE_DIR)+"/static/face_detect"
JSON_DATA_PATH = str(BASE_DIR)+"/data_recognition"
# Create your views here.
class CustomIsAdminUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)



def check_time_in_range(start, end, x):
    start = str(start)
    end = str(end)
    x = str(x)
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    x = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    return start <= x <= end


def get_data_recognition(find_date):
    try:
        with open(f"{JSON_DATA_PATH}/{find_date}.json") as f:
            data = json.load(f)
    except:
        data = []
    return data
# get_infor_face_img: return [{
# face_name:
# time:
# }]


class Recognition(APIView):
    permission_classes = [CustomIsAdminUser]
    def get(self, request, find_date=str(date.today()), total=10):
        list_unknow = []
        list_success = []
        list_not_success = []
        data_recog = get_data_recognition(find_date)
        find_date = datetime.strptime(find_date,"%Y-%m-%d")
        registration_schedule = RoomOrder.objects.filter(
            start_time__gte=str(find_date))[:total]
        for item in data_recog:
            item['status'] = ''
            for i in registration_schedule:
                if item['name'] == i.user.full_name:
                    if check_time_in_range(i.start_time, i.end_time, item['time']):
                        item['status'] = 'pass'
                    else:
                        item['status'] = 'wrong shift'
            print(">>>>>>>",item)
            if item['name'] == 'unknow':
                list_unknow.append(item)
            if item['status'] == 'pass':
                list_success.append(item)
            if item['status'] == 'wrong shift':
                list_not_success.append(item)
        data = {'list_unknow': list_unknow,
                'list_success': list_success,
                'list_not_success': list_not_success}

        return JsonResponse(data)
