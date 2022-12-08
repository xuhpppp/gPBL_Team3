from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from mysite.settings import BASE_DIR
from datetime import datetime,date
import os
from room.models import RoomOrder

FACE_DETECT_DIRS = str(BASE_DIR)+"\\static\\face_detect"

# Create your views here.
def get_infor_face_img(find_date): # type find_date: YYYY-MM-DD
	infor = []
	list_file = os.listdir(f"{FACE_DETECT_DIRS}\\{find_date}")
	for file in list_file:
		new_name_file = file.split('_')
		item = {}
		item['face_name'] = new_name_file[0]
		item['file_name'] = file
		item['time'] = datetime.fromtimestamp(float(new_name_file[1][0:-4])).strftime('%Y-%m-%d %H:%M:%S')
		infor.sort(key=lambda x: x['time'], reverse=True)
	return infor

#get_infor_face_img: return [{
# 	face_name:
#	time:
# }]


class Recognition(APIView):
	def get(self,request, find_date=str(date.today())):
		data = get_infor_face_img(find_date)
		registration_schedule = RoomOrder.objects.all()
		
