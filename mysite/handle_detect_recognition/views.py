from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from mysite.settings import BASE_DIR
from datetime import datetime, date, timezone
import os
from room.models import RoomOrder
import json

FACE_DETECT_PATH = str(BASE_DIR)+"\\static\\face_detect"
JSON_DATA_PATH = str(BASE_DIR)+"data_recognition"
# Create your views here.

def check_time_in_range(start, end, x):
    start = datetime.strptime(start, '%Y/%m/%d %H:%M+%z')
    end = datetime.strptime(end, '%Y/%m/%d %H:%M+%z')
    x = datetime.strptime(x, '%Y/%m/%d %H:%M+%z')

    return start <= x <= end


def get_data_recognition(find_date):
    try:
        with open(f"{JSON_DATA_PATH}/{find_date}.json") as f:
            data = json.load(f)
    except:
        data = []
    return data
# get_infor_face_img: return [{
#face_name:
# time:
# }]

def time_in_range(start, end, x):
    today = timezone.localtime().date()
    start = timezone.make_aware(datetime.datetime.combine(today, start))
    end = timezone.make_aware(datetime.datetime.combine(today, end))
    x = timezone.make_aware(datetime.datetime.combine(today, x))
    if end <= start:
        end += datetime.timedelta(days=1) # tomorrow!
    if x <= start:
        x += datetime.timedelta(days=1) # tomorrow!
    return start <= x <= end


class Recognition(APIView):
    def get(self, request, find_date=str(date.today())):
        data_recog = get_data_recognition(find_date)
        registration_schedule = RoomOrder.objects.filter(start_time__gte=str(datetime.now()))

        for item in data_recog:
            for i in registration_schedule:
                if item['name'] == i.user.full_name:
                    
                else:
                    pass

