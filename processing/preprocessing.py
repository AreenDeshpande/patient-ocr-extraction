import os
import json
import easyocr
import sqlite3
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

read = easyocr.Reader(['en'])

#preprocessing
def preprocess_image(image):
    gray=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
    blur=cv2.GaussianBlur(gray,(5,5),0)
    img=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return img
#ocr extraction function
def extract_text_jpg(image):
    preprocessed_image=preprocess_image(image)
    text=read.readtext(preprocessed_image,detail=0)
    return " ".join(text)

def extract_text_pdf(pdf_file):
    image=convert_from_path(pdf_file)
    extracted_text=[]
    for img in image:
        img=np.array(img)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        processed_img=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        text=read.readtext(processed_img,detail=0)
        extracted_text.append(" ".join(text))
    return " ".join(extracted_text)



