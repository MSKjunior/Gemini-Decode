import os
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import base64
import google.generativeai as genai


load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")
print(f" Loaded API Key: {api_key}")  


genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-pro')

def get_response(input_text, image):
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Gemini Decode: Multilanguage Document Extraction by Group 17")
st.header("Gemini Decode: Multilanguage Document Extraction by Gemini Pro")


def set_background(image_file):
    with open(image_file, "rb") as img:
        b64_image = base64.b64encode(img.read()).decode("utf-8")
    css = f"""
    <style>
    .stApp {{
        background: url(data:image/png;base64,{b64_image});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    
input_prompt = st.text_input("Input:", key="input")
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


submit = st.button("Submit")

text = ("Utilizing Gemini Pro AI, this project effortlessly extracts vital information from diverse multilingual documents, "
        "transcending language barriers with precision and efficiency for enhanced productivity and decision-making.")
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

if submit and image is not None:
    response = get_response(input_prompt, image)  
    st.subheader("Group 17 Response:")
    st.write(response)