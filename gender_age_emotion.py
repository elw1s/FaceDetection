# SPDX-License-Identifier: Apache-2.0

import cv2
import onnxruntime as ort
import argparse
import numpy as np
import sys
from PIL import Image
sys.path.append('..')
from ultraface.dependencies.box_utils import predict

# ------------------------------------------------------------------------------------------------------------------------------------------------
# Face detection using UltraFace-640 onnx model
face_detector_onnx = "C:/Users/Arda/Desktop/Test/WebcamTest/ultraface/models/version-RFB-640.onnx"

# Start from ORT 1.10, ORT requires explicitly setting the providers parameter if you want to use execution providers
# other than the default CPU provider (as opposed to the previous behavior of providers getting set/registered by default
# based on the build flags) when instantiating InferenceSession.
# For example, if NVIDIA GPU is available and ORT Python package is built with CUDA, then call API as following:
# ort.InferenceSession(path/to/model, providers=['CUDAExecutionProvider'])
face_detector = ort.InferenceSession(face_detector_onnx)

# scale current rectangle to box
def scale(box):
    width = box[2] - box[0]
    height = box[3] - box[1]
    maximum = max(width, height)
    dx = int((maximum - width)/2)
    dy = int((maximum - height)/2)

    bboxes = [box[0] - dx, box[1] - dy, box[2] + dx, box[3] + dy]
    return bboxes

# crop image
def cropImage(image, box):
    num = image[box[1]:box[3], box[0]:box[2]]
    return num

# face detection method
def faceDetector(orig_image, threshold = 0.7):
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (640, 480))
    cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/face.jpg", image)
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)


    input_name = face_detector.get_inputs()[0].name
    confidences, boxes = face_detector.run(None, {input_name: image})
    boxes, labels, probs = predict(orig_image.shape[1], orig_image.shape[0], confidences, boxes, threshold)
    return boxes, labels, probs
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Face gender classification using GoogleNet onnx model
gender_classifier_onnx = "C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/models/gender_googlenet.onnx"

# Start from ORT 1.10, ORT requires explicitly setting the providers parameter if you want to use execution providers
# other than the default CPU provider (as opposed to the previous behavior of providers getting set/registered by default
# based on the build flags) when instantiating InferenceSession.
# For example, if NVIDIA GPU is available and ORT Python package is built with CUDA, then call API as following:
# ort.InferenceSession(path/to/model, providers=['CUDAExecutionProvider'])
gender_classifier = ort.InferenceSession(gender_classifier_onnx)
genderList=['Male','Female']

# gender classification method
def genderClassifier(orig_image):
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/gender.jpg", image)
    image_mean = np.array([104, 117, 123])
    image = image - image_mean
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)

    input_name = gender_classifier.get_inputs()[0].name
    genders = gender_classifier.run(None, {input_name: image})
    gender = genderList[genders[0].argmax()]
    return gender
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Face age classification using GoogleNet onnx model
age_classifier_onnx = "C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/models/age_googlenet.onnx"

# Start from ORT 1.10, ORT requires explicitly setting the providers parameter if you want to use execution providers
# other than the default CPU provider (as opposed to the previous behavior of providers getting set/registered by default
# based on the build flags) when instantiating InferenceSession.
# For example, if NVIDIA GPU is available and ORT Python package is built with CUDA, then call API as following:
# ort.InferenceSession(path/to/model, providers=['CUDAExecutionProvider'])
age_classifier = ort.InferenceSession(age_classifier_onnx)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

# age classification method
def ageClassifier(orig_image):
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))

    cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/age.jpg", image)

    image_mean = np.array([104, 117, 123])
    image = image - image_mean
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)

    input_name = age_classifier.get_inputs()[0].name
    ages = age_classifier.run(None, {input_name: image})
    age = ageList[ages[0].argmax()]
    return age

# emotion classification
emotion_classifier_onnx = "C:/Users/Arda/Desktop/Test/WebcamTest/emotion_ferplus/model/emotion-ferplus-8.onnx"
emotion_classifier = ort.InferenceSession(emotion_classifier_onnx)
emotionList = ['neutral', 'happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear', 'contempt']

def emotionClassfier(orig_image):
    #image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    #image = cv2.resize(image, (64, 64))
    #image_mean = np.array([104, 117, 123])
    #image = image - image_mean
    #image = np.transpose(image, [2, 0, 1])
    #image = np.expand_dims(image, axis=0)
    #image = image.astype(np.float32)

    input_shape = (1, 1, 64, 64)
    img = cv2.cvtColor(orig_image , cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (64, 64), Image.ANTIALIAS)

    cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/emotion.jpg", img)
    img_data = np.array(img)
    img_data = np.resize(img_data, input_shape)

    img_data = img_data.astype(np.float32)

    input_name = emotion_classifier.get_inputs()[0].name
    emotions = emotion_classifier.run(None,{input_name: img_data})
    emotion = emotionList[emotions[0].argmax()]
    return emotion

# ------------------------------------------------------------------------------------------------------------------------------------------------
# Main void

parser=argparse.ArgumentParser()
parser.add_argument("-i", "--image", type=str, required=False, help="input image")
args=parser.parse_args()

#img_path = args.image if args.image else "C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/fear.jpg"
color = (255, 128, 0)

capture = cv2.VideoCapture(0)  
while True :
    _, frame =capture.read()
    #orig_image = cv2.imread(frame)
    #boxes, labels, probs = faceDetector(orig_image)
    #cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/input.jpg", orig_image)
    boxes, labels, probs = faceDetector(frame)

    for i in range(boxes.shape[0]):
        box = scale(boxes[i, :])
        cropped = cropImage(frame, box)
        #cropped = cropImage(orig_image, box)
        gender = genderClassifier(cropped)
        age = ageClassifier(cropped)
        emotion = emotionClassfier(cropped)

        print(f'Box {i} --> {gender}, {age} , {emotion}')

        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 4)
        cv2.putText(frame, f'{gender}, {age} , {emotion}', (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.imshow('', frame)

        #cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), color, 4)
        #cv2.putText(orig_image, f'{gender}, {age} , {emotion}', (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        #cv2.imshow('', orig_image)
        #cv2.imwrite("C:/Users/Arda/Desktop/Test/WebcamTest/age_gender/dependencies/output/output.jpg", orig_image)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

capture.release() 
cv2.destroyAllWindows()
# ------------------------------------------------------------------------------------------------------------------------------------------------