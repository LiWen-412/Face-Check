# import django
#
# from PIL import Image
# from numpy import asarray
# from numpy import expand_dims
# from celery import task
#
# django.setup()
# Detector = None
# Model2 = None
#
#
# @task(name="get_face_feature")
# def get_face_feature(image):
#     global Detector
#     global Model2
#     if Detector is None:
#         from mtcnn.mtcnn import MTCNN
#         from keras.models import load_model
#         Detector = MTCNN()
#         Model2 = load_model('facenet_keras.h5')
#     required_size = (160, 160)
#     pixels = asarray(image)
#     results = Detector.detect_faces(pixels)
#     if len(results) > 0:
#         x1, y1, width, height = results[0]["box"]
#         # bug fix
#         x1, y1 = abs(x1), abs(y1)
#         x2, y2 = x1 + width, y1 + height
#         # extract the face
#         face = pixels[y1:y2, x1:x2]
#         # resize pixels to the model size
#         image = Image.fromarray(face)
#         image = image.resize(required_size)
#         face_array = asarray(image)
#
#         face_pixels = face_array.astype('float32')
#         # standardize pixel values across channels (global)
#         mean, std = face_pixels.mean(), face_pixels.std()
#         face_pixels = (face_pixels - mean) / std
#         # transform face into one sample
#         samples = expand_dims(face_pixels, axis=0)
#         # make prediction to get embedding
#
#         face_feature = Model2.predict(samples)
#         return [results, face_feature]
#
#
# from numpy import load
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import Normalizer
# from sklearn.svm import SVC
# import pickle
# from .models import User
#
#
# def fit_svm():
#     users = User.objects.all().values("username", "feature1", "feature2", "feature3")
#     all_user_features = []
#     all_user_name = []
#     for x in users:
#         if x["feature1"] == "":
#             continue
#         all_user_features.append(eval(x["feature1"]))
#         all_user_features.append(eval(x["feature2"]))
#         all_user_features.append(eval(x["feature3"]))
#         all_user_name.append(x["username"])
#         all_user_name.append(x["username"])
#         all_user_name.append(x["username"])
#     in_encoder = Normalizer(norm='l2')
#     trainX = in_encoder.transform(all_user_features)
#     out_encoder = LabelEncoder()
#     out_encoder.fit(all_user_name)
#     trainy = out_encoder.transform(all_user_name)
#     model = SVC(kernel='linear', probability=True)
#     model.fit(trainX, trainy)
#
#     with open("svm.plk", "wb") as f:
#         model = pickle.dumps(model)
#         f.write(model)
#     with open("out_encoder.plk", "wb") as f:
#         out_encoder = pickle.dumps(out_encoder)
#         f.write(out_encoder)
