from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from mysite.settings import BASE_DIR
from datetime import datetime, date, timezone
import os
from room.models import RoomOrder
import json

FACE_DETECT_PATH = str(BASE_DIR)+"/static/face_detect"
JSON_DATA_PATH = str(BASE_DIR)+"/data_recognition"
# Create your views here.


def check_time_in_range(start, end, x):
    start = datetime.strptime(start[:-6], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end[:-6], '%Y-%m-%d %H:%M:%S')
    x = datetime.strptime(x[:-6], '%Y-%m-%d %H:%M:%S')

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


def time_in_range(start, end, x):
    today = timezone.localtime().date()
    start = timezone.make_aware(datetime.datetime.combine(today, start))
    end = timezone.make_aware(datetime.datetime.combine(today, end))
    x = timezone.make_aware(datetime.datetime.combine(today, x))
    if end <= start:
        end += datetime.timedelta(days=1)  # tomorrow!
    if x <= start:
        x += datetime.timedelta(days=1)  # tomorrow!
    return start <= x <= end


class Recognition(APIView):
    def get(self, request, find_date=str(date.today()), total=10):
        list_unknow = []
        list_success = []
        list_not_success = []

        data_recog = get_data_recognition(find_date)
        registration_schedule = RoomOrder.objects.filter(
            start_time__gte=str(datetime.now()))

        for item in data_recog:
            for i in registration_schedule:
                print('>>>>>>',item['name'])
                if item['name'] == i.user.full_name:
                    if check_time_in_range(i.start_time, i.end_time, item['time']):
                        list_success.append(item)
                    else:
                        list_not_success.append(item)

            if item['name'] == 'unknow':
                    list_unknow.append(item)
        data = {'list_unknow': list_unknow,
                'list_success': list_success,
                'list_not_success': list_not_success}

        return JsonResponse(data)
