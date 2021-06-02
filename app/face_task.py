import cv2
import numpy as np
from .models import User
import sys
import face_recognition

from numpy import expand_dims

from PIL import Image, ImageDraw, ImageFont
import dlib

face_encodings = None
usernames = None


def cv2ImgAddText(img, text, left, top, textColor=(255,0 , 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "yh.ttf", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def get_face_encoding(imgs):  # 传来的是 numpy数组
    """ 人脸识别 """
    checked_users = []
    face_locations = face_recognition.face_locations(imgs)
    unknown_face_encodings = face_recognition.face_encodings(imgs)
    for i in range(len(unknown_face_encodings)):
        unknown_encoding = unknown_face_encodings[i]
        face_location = face_locations[i]
        top, right, bottom, left = face_location
        cv2.rectangle(imgs, (left, top), (right, bottom), (0, 255, 0), 2)
        face_distances = np.linalg.norm(face_encodings - unknown_encoding, axis=1)  # 计算距离
        best_match_index = np.argmin(face_distances)  # 找到最相似的人
        if face_distances[best_match_index] < 6:  # 对比人脸特征必须  必须小于6 想要更准确的人脸 可以减小这个值
            name = usernames[best_match_index]

            checked_users.append(name)
            imgs = cv2ImgAddText(imgs, name, left - 10, top - 10, (255, 0, 0), 15)


    return imgs, checked_users


def encode_face_ing(imgs):
    _encodings = []
    for img in imgs:
        encoding = face_recognition.face_encodings(img)
        if encoding:
            _encodings.append(encoding[0])
    return _encodings


def load_local_face():
    import glob
    images = glob.glob("data/*/*.jpeg")
    names = []
    face_encodings = []
    for x in images:
        image = face_recognition.load_image_file(x)

        encoding = face_recognition.face_encodings(image)
        if encoding:
            print(x)
            names.append(x.split("\\")[-2])
            face_encodings.append(encoding[0])
    face_encodings = np.array(face_encodings)
    print(face_encodings.shape, names)

    for x in list(set(names)):
        User.objects.create_user(username=x,
                                 password="1234567890",
                                 face_id=usernames.index(x))
    np.save("names.npy", np.array(names))
    np.save("face_encodings.npy", face_encodings)


if "runserver" in sys.argv:
    face_encodings = np.load("face_encodings.npy")
    usernames = np.load("names.npy")
    print("载入已知人脸", face_encodings.shape, usernames.shape)
