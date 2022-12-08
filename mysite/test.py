import os
from datetime import datetime

def get_list_face_img(find_date): # type find_date: YYYY-MM-DD
	infor = []
	list_file = os.listdir(find_date)
	for file in list_file:
		new_name_file = file.split('_')
		item = {}
		item['face_name'] = new_name_file[0]
		item['file_name'] = file
		item['time'] = datetime.fromtimestamp(float(new_name_file[1][0:-4])).strftime('%Y-%m-%d %H:%M:%S')
		infor.append(item)

	infor.sort(key=lambda x: x['time'], reverse=True)
	
	return infor

print(get_list_face_img('C:\\Users\\admin\\Documents\\Workspace\\Python\\gPBL_Team3\\mysite\\static\\face_detect\\2022-12-08'))