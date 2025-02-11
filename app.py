import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import os

from processing.preprocessing import preprocess_image , extract_text_pdf , extract_text_jpg

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