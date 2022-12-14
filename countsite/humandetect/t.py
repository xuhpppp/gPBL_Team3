import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.classes = 0
model.imgsz = 320

cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()

    results = model(frame, size=320)
    persons = results.pandas().xyxy[0].value_counts('name')

    cv2.imshow('Detection', frame)
    if len(persons):
        print('oke')

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)