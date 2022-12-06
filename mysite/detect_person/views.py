import torch
import numpy as np
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

# Create your views here.


def index(request):
    return render(request, 'index.html')

def get_video():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s',
                        pretrained=True, force_reload=True)

    cap = cv2.VideoCapture(0)

    old_count_person = 0
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 400))
        results = model(frame)
        frame = np.squeeze(results.render())
        cv2.imshow('FRAME', frame)
        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')
        # if cv2.waitKey(20) & 0xFF == ord('q'):
        #     break
        # new_count_person = (results.pandas().xyxy[0])['name']
        # try:
        #     new_count_person = (new_count_person.value_counts())['person']
        # except:
        #     new_count_person = 0
        # if old_count_person != new_count_person:
        #     print(new_count_person, ' person')
        #     old_count_person = new_count_person

    cap.release()
    cv2.destroyAllWindows()

def webcam_stream(request):
    print('>>>>>>>>>>>>Stream >>>>>>>>>>>>>>>>')
    return StreamingHttpResponse(get_video(), content_type='multipart/x-mixed-replace; boundary=frame')
