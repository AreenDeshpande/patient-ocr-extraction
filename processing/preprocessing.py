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
def preprocess_image(image_path):
    image=cv2.imread(image_path ,cv2.IMREAD_GRAYSCALE)
    image=cv2.GaussianBlur(image,(5,5),0)
    image=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return image
#ocr extraction function
def extract_text_jpg(image_path):
    preprocessed_image=preprocess_image(image_path)
    text=read.readtext(preprocessed_image,detail=0)
    return " ".join(text)

def extract_text_pdf(pdf_path):
    image=convert_from_path(pdf_path)
    extracted_text=[]
    for img in image:
        img=np.array(img)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        processed_img=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        text=read.readtext(processed_img,detail=0)
        extracted_text.append(" ".join(text))
    return " ".join(extracted_text)



