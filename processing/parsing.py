
import os
import json
import easyocr
import sqlite3
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

def parse_text(text):
    parsed_data={
        "patient_name":"None" ,
        "age":"None" ,
        "diagnosis":"None"
    }

    lines=text.split('\n')
    for line in lines:
        if "Name:" in line:
            parsed_data["patient_name"]=line.split("Name:")[-1].strip()
        elif "Age:" in line:
            parsed_data["age"]=line.split("Age:")[-1].strip()
        elif "Diagnosis:" in line:
            parsed_data["diagnosis"]=line.split("Diagnosis:")[-1].strip()

    return parsed_data

def store_in_db(data,db_name="patient_data.db"):
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS patient_info(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   patient_name TEXT,
                   age TEXT,
                   diagnosis TEXT)''')
    
    cursor.execute('''
                   INSERT INTO patient_info(patient_name,age,diagnosis)
                     VALUES(?,?,?)''',(data["patient_name"],data["age"],data["diagnosis"]))
    conn.commit
    conn.close()