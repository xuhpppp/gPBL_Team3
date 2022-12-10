from channels.generic.websocket import WebsocketConsumer

from django.shortcuts import get_object_or_404

#pytorch
from concurrent.futures import thread
import torch
from torchvision import transforms
import time
from threading import Thread
import json
from datetime import datetime

#other lib
import sys
import numpy as np
import os
import shutil
import cv2

from authen.models import User
from room.models import RoomOrder
from room.serializers import RoomOrderSerializer
sys.path.append("..")

yolo_path = os.path.realpath(os.path.join(sys.path[0], 'face\\yolov5_face'))
sys.path.insert(0, yolo_path)
#import pdb; pdb.set_trace()
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression_face, scale_coords

# Check device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Get model detect
## Case 1:
# model = attempt_load("yolov5_face/yolov5s-face.pt", map_location=device)

## Case 2:
model = attempt_load(yolo_path + "\\yolov5n-0.5.pt", map_location=device)

# Get model recognition
## Case 1: 
from .insightface.insight_face import iresnet100
weight = torch.load(yolo_path + "\\..\\insightface\\resnet100_backbone.pth", map_location = device)
model_emb = iresnet100()

## Case 2: 
# from insightface.insight_face import iresnet18
# weight = torch.load("insightface/resnet18_backbone.pth", map_location = device)
# model_emb = iresnet18()

model_emb.load_state_dict(weight)
model_emb.to(device)
model_emb.eval()

face_preprocess = transforms.Compose([
                                    transforms.ToTensor(), # input PIL => (3,56,56), /255.0
                                    transforms.Resize((112, 112)),
                                    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
                                    ])

isThread = True
total_thread = 0
online_users = []
faces = 0
score = 0
name = None
stop = 0

# Resize image
def resize_image(img0, img_size):
    h0, w0 = img0.shape[:2]  # orig hw
    r = img_size / max(h0, w0)  # resize image to img_size

    if r != 1:  # always resize down, only resize up if training with augmentation
        interp = cv2.INTER_AREA if r < 1  else cv2.INTER_LINEAR
        img0 = cv2.resize(img0, (int(w0 * r), int(h0 * r)), interpolation=interp)

    imgsz = check_img_size(img_size, s=model.stride.max())  # check img_size
    img = letterbox(img0, new_shape=imgsz)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1).copy()  # BGR to RGB, to 3x416x416

    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    
    return img

def scale_coords_landmarks(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2, 4, 6, 8]] -= pad[0]  # x padding
    coords[:, [1, 3, 5, 7, 9]] -= pad[1]  # y padding
    coords[:, :10] /= gain
    #clip_coords(coords, img0_shape)
    coords[:, 0].clamp_(0, img0_shape[1])  # x1
    coords[:, 1].clamp_(0, img0_shape[0])  # y1
    coords[:, 2].clamp_(0, img0_shape[1])  # x2
    coords[:, 3].clamp_(0, img0_shape[0])  # y2
    coords[:, 4].clamp_(0, img0_shape[1])  # x3
    coords[:, 5].clamp_(0, img0_shape[0])  # y3
    coords[:, 6].clamp_(0, img0_shape[1])  # x4
    coords[:, 7].clamp_(0, img0_shape[0])  # y4
    coords[:, 8].clamp_(0, img0_shape[1])  # x5
    coords[:, 9].clamp_(0, img0_shape[0])  # y5
    return coords

def get_face(input_image):
    # Parameters
    size_convert = 128
    conf_thres = 0.4
    iou_thres = 0.5
    
    # Resize image
    img = resize_image(input_image.copy(), size_convert)

    # Via yolov5-face
    with torch.no_grad():
        pred = model(img[None, :])[0]

    # Apply NMS
    det = non_max_suppression_face(pred, conf_thres, iou_thres)[0]
    bboxs = np.int32(scale_coords(img.shape[1:], det[:, :4], input_image.shape).round().cpu().numpy())
    
    landmarks = np.int32(scale_coords_landmarks(img.shape[1:], det[:, 5:15], input_image.shape).round().cpu().numpy())    
    
    return bboxs, landmarks

def get_feature(face_image, training = True): 
    # Convert to RGB
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    
    # Preprocessing image BGR
    face_image = face_preprocess(face_image).to(device)
    
    # Via model to get feature
    with torch.no_grad():
        if training:
            emb_img_face = model_emb(face_image[None, :])[0].cpu().numpy()
        else:
            emb_img_face = model_emb(face_image[None, :]).cpu().numpy()
    
    # Convert to array
    images_emb = emb_img_face/np.linalg.norm(emb_img_face)
    return images_emb

def read_features(root_fearure_path = yolo_path + "\\..\\static\\feature\\face_features.npz"):
    data = np.load(root_fearure_path, allow_pickle=True)
    images_name = data["arr1"]
    images_emb = data["arr2"]
    
    return images_name, images_emb

def recognition(face_image):
    global isThread, score, name
    start = time.time()
    # Get feature from face
    query_emb = (get_feature(face_image, training=False))
    
    # Read features
    images_names, images_embs = read_features()   

    scores = (query_emb @ images_embs.T)[0]

    id_min = np.argmax(scores)
    score = scores[id_min]
    name = images_names[id_min]
    isThread = True
    print("successful")
    print(start - time.time())

def recognition_mutiple(image):
    global total_thread, online_users, faces
    # Get faces
    bboxs, _ = get_face(image)
    if faces != len(bboxs):
        online_users.clear()
    # Get boxs
    for i in range(len(bboxs)):
        # Get location face
        x1, y1, x2, y2 = bboxs[i]

        # Get face from location
        face_image = image[y1:y2, x1:x2]
        
        # Get feature from face
        query_emb = (get_feature(face_image, training=False))
        
        # Read features
        images_names, images_embs = read_features()   
        
        scores = (query_emb @ images_embs.T)[0]

        id_min = np.argmax(scores)
        score = scores[id_min]
        name = images_names[id_min]
        
        if len(online_users) < len(bboxs):
            if score <= 0.2:
                online_users.append('unknown')
            elif score > 0.2 and name not in online_users:
                online_users.append(name)
        else:
            if score > 0.2 and name not in online_users:
                online_users.remove('unknown')
                online_users.append(name)

    faces = len(bboxs)
    total_thread -= 1
    return image

class RecognizeConsumer(WebsocketConsumer):
    def main(self):
        global total_thread, online_users, stop
        
        # for re-opening camera
        stop = 0

        # Open camera 
        cap = cv2.VideoCapture(0)
        start = time.time_ns()
        frame_count = 0
        fps = -1
        
        # Save video
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        
        size = (frame_width, frame_height)
        video = cv2.VideoWriter('./static/results/face-recognition2.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 6, size)
        
        # Read until video is completed
        while(stop == 0):
            # Capture frame-by-frame
            _, frame = cap.read()
            
            
            if total_thread < 1:
                total_thread += 1
                thread = Thread(target=recognition_mutiple, args=(frame,))
                thread.start()
            # Get faces
            bboxs, landmarks = get_face(frame)
            # h, w, c = frame.shape
            
            # tl = 1 or round(0.002 * (h + w) / 2) + 1  # line/font thickness
            # clors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255)]
            
            # # Get boxs
            for i in range(len(bboxs)):
            #     # Get location face
                x1, y1, x2, y2 = bboxs[i]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 146, 230), 2)
                
            
            # Count fps 
            frame_count += 1
            
            if frame_count >= 30:
                end = time.time_ns()
                fps = 1e9 * frame_count / (end - start)
                frame_count = 0
                start = time.time_ns()
        
            if fps > 0:
                fps_label = "FPS: %.2f" % fps
                lable_msg = f"{fps_label} Online users: {','.join(online_users)}"
                cv2.putText(frame, lable_msg, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # print(online_users)
            self.send(json.dumps({
                'online_users': online_users
            }))
            video.write(frame)
            cv2.imshow("Face Recognition", frame)
            
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break  
        
        video.release()
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(0)

    def connect(self):
        self.accept()

        # assume that we only use room 101
        list_of_RoomOrder = RoomOrder.objects.all().filter(room_name='101').filter(end_time__gt=datetime.now())

        if (len(list_of_RoomOrder) > 0):
            serializer = RoomOrderSerializer(list_of_RoomOrder[0], many=False)

            self.send(json.dumps({
                'next_order': serializer.data,
                'online_users': online_users
            }))
        else:
            self.send(json.dumps({
                'next_order': 'There is no order!',
                'online_users': online_users
            }))

        recognize_thread = Thread(target=self.main)
        recognize_thread.start()

    def disconnect(self, code):
        global stop
        stop = 1
        print('close')

def capture_frame():
    global stop
    # for re-opening camera
    stop = 0
    cap = cv2.VideoCapture(0)

    count = 0
    while stop == 0:
        _, frame = cap.read()

        cv2.imshow('Scanning', frame)

        if count % 10 == 0:
            cv2.imwrite('mysite\\face\\scan-result\\' + str(count) + '.jpg', frame)
        count += 1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(0)

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s = ''
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

def get_face_training(input_image):
    # Parameters
    size_convert = 256
    conf_thres = 0.4
    iou_thres = 0.5
    
    # Resize image
    img = resize_image(input_image.copy(), size_convert)

    # Via yolov5-face
    with torch.no_grad():
        pred = model(img[None, :])[0]

    # Apply NMS
    det = non_max_suppression_face(pred, conf_thres, iou_thres)[0]
    bboxs = np.int32(scale_coords(img.shape[1:], det[:, :4], input_image.shape).round().cpu().numpy())
    
    return bboxs

def read_features_training(root_fearure_path = yolo_path + "\\..\\static\\feature\\face_features.npz"):
    try:
        data = np.load(root_fearure_path + ".npz", allow_pickle=True)
        images_name = data["arr1"]
        images_emb = data["arr2"]
        
        return images_name, images_emb
    except:
        return None

def training(full_training_dir='mysite\\face\\database\\full-training-datasets\\',
             additional_training_dir='mysite\\face\\database\\additional-training-datasets\\', 
             faces_save_dir='mysite\\face\\database\\face-datasets\\',
             features_save_dir='mysite\\face\\static\\feature\\face_features', 
             is_add_user=True):
    
    # Init results output
    images_name = []
    images_emb = []
    
    # Check mode full training or additidonal
    if is_add_user == True:
        source = additional_training_dir
    else:
        source = full_training_dir
    
    # Read train folder, get and save face 
    for name_person in os.listdir(source):
        person_image_path = os.path.join(source, name_person)
        
        # Create path save person face
        person_face_path = os.path.join(faces_save_dir, name_person)
        os.makedirs(person_face_path, exist_ok=True)
        
        for image_name in os.listdir(person_image_path):
            if image_name.endswith(("png", 'jpg', 'jpeg')):
                image_path = person_image_path + f"/{image_name}"
                input_image = cv2.imread(image_path)  # BGR 

                # Get faces
                bboxs = get_face_training(input_image)

                # Get boxs
                for i in range(len(bboxs)):
                    # Get number files in person path
                    number_files = len(os.listdir(person_face_path))

                    # Get location face
                    x1, y1, x2, y2 = bboxs[i]

                    # Get face from location
                    face_image = input_image[y1:y2, x1:x2]

                    # Path save face
                    path_save_face = person_face_path + f"/{number_files}.jpg"
                    
                    # Save to face database 
                    cv2.imwrite(path_save_face, face_image)
                    
                    # Get feature from face
                    images_emb.append(get_feature(face_image, training=True))
                    images_name.append(name_person)
    
    # Convert to array
    images_emb = np.array(images_emb)
    images_name = np.array(images_name)
    
    features = read_features_training(features_save_dir) 
    if features is None or is_add_user== False:
        pass
    else:        
        # Read features
        old_images_name, old_images_emb = features  
    
        # Add feature and name of image to feature database
        images_name = np.hstack((old_images_name, images_name))
        images_emb = np.vstack((old_images_emb, images_emb))
        
        print("Update feature!")
    
    # Save features
    np.savez_compressed(features_save_dir, 
                        arr1 = images_name, arr2 = images_emb)
    
    # Move additional data to full train data
    if is_add_user == True:
        for sub_dir in os.listdir(additional_training_dir):
            dir_to_move = os.path.join(additional_training_dir, sub_dir)
            shutil.move(dir_to_move, full_training_dir, copy_function = shutil.copytree)

    print('finish!')

class InsertConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        # capture frame
        scanning_thread = Thread(target=capture_frame)
        scanning_thread.start()

    def receive(self, text_data):
        user = get_object_or_404(User, id=text_data)

        words = user.full_name.split(' ')
        filename = remove_accents(words[-1])
        for i in range(0, len(words) - 1):
            filename += remove_accents(words[i])[0]
        filename += '-' + str(user.id)

        additional_path = os.path.realpath(os.path.join(sys.path[0], '..\\database\\additional-training-datasets\\' + filename))
        if os.path.exists(additional_path) == False:
            os.makedirs(additional_path)
        
        src_path = os.path.realpath(os.path.join(sys.path[0], '..\\scan-result'))
        allfiles = os.listdir(src_path)
        for f in allfiles:
            shutil.move(os.path.join(src_path, f), os.path.join(additional_path, f))
    
    def disconnect(self, code):
        global stop
        stop = 1

        training_thread = Thread(target=training)
        training_thread.start()

        print('close')