import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import os
from processing.parsing import parse_text ,store_in_db
from processing.preprocessing import preprocess_image , extract_text_pdf , extract_text_jpg
import sqlite3
st.title('Data Processing App')

st.sidebar.header("Upload data")
uploaded_file = st.sidebar.file_uploader("Upload an Image or PDF", type=["jpg", "png", "jpeg", "pdf"])
if uploaded_file:
    extension=uploaded_file.name.split('.')[-1].lower()
    if extension in ['jpg','png','jpeg']:
        image=Image.open(uploaded_file)
        img_np=np.array(image)
        fin_img=preprocess_image(img_np)
        extracted_text=extract_text_jpg(fin_img)
    
    elif extension == "pdf":
        temp_path = "temp.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        extracted_text = extract_text_pdf(temp_path)
        os.remove(temp_path)

    parsed_text=parse_text(extracted_text)
    st.subheader("Extracted data")
    st.json(parsed_text)

    store_in_db(parsed_text)
    st.success("Data stored in database successfully")

#query
st.sidebar.header("Query data")
search_name=st.sidebar.text_input("Enter patient name")
if st.sidebar.button("Search"):
    conn = sqlite3.connect("patient_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_info WHERE patient_name LIKE ?", (f"%{search_name}%",))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        st.subheader("Search Results")
        for row in results:
            st.write({"ID": row[0], "Name": row[1], "Age": row[2], "Diagnosis": row[3]})
    else:
        st.warning("No patient found with that name.")