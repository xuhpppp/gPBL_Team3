from channels.generic.websocket import WebsocketConsumer

import torch
import cv2
import json
from threading import Thread
import torchvision

stop = 0

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.classes = 0
model.imgsz = 320

class CountConsumer(WebsocketConsumer):
    def run(self):
        global stop
        stop = 0
        
        cap = cv2.VideoCapture(1)

        while stop != 1:
            _, frame = cap.read()

            results = model(frame, size=320)
            persons = results.pandas().xyxy[0].value_counts('name')

            # for row in results.pandas().xyxy[0].iterrows():
            #     print(row[1])
            #torchvision.utils.draw_bounding_boxes(frame)
            cv2.imshow('Detection', frame)
            cv2.waitKey(1)
            
            if len(persons):
                self.send(json.dumps({
                    'log': f"There are {persons['person']} person in the room now"
                }))
            else:
                self.send(json.dumps({
                    'log': "There is no one in the room now"
                }))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break  

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(0)

    def connect(self):
        self.accept()
        print(1)

        run_thread = Thread(target=self.run)
        run_thread.start()

    def disconnect(self, code):
        global stop
        stop = 1

        print(0)