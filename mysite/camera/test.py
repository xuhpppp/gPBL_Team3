import os
from datetime import date
date_today = str(date.today())
path = f"../static/face_detect/{date_today}"

if not os.path.exists(path):
	path = os.makedirs(path)