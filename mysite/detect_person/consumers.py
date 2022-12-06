import json
import cv2
import torch
import numpy as np

from channels.generic.websocket import WebsocketConsumer


class DetectConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': "Loading...."
        }))
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
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            new_count_person = (results.pandas().xyxy[0])['name']
            try:
                new_count_person = (new_count_person.value_counts())['person']
            except:
                new_count_person = 0
            if old_count_person != new_count_person:
                self.send(text_data=json.dumps({
                    'count_persons': int(new_count_person)
                    }))
                print(new_count_person)
                old_count_person = new_count_person

        cap.release()
        cv2.destroyAllWindows()

    def disconnect(self, close_code):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

