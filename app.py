# -*- coding: utf-8 -*-
"""Untitled35.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XIuLDM6SqTOk8-yjeNqMpC1uOkk3ziBq
"""

#!pip install -q -U google-generativeai
#!pip install PyPDF2
#!pip install streamlit

import streamlit as st
import os
import shutil
import google.generativeai as genai
from PyPDF2 import PdfReader

# Set your Google API key
GOOGLE_API_KEY = "AIzaSyDJmXWub0e8R664vzjHC7mnmmcu9c5P0Y0"

# Configure generativeai with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the GenerativeModel
model = genai.GenerativeModel('gemini-pro')

# Function to save uploaded PDF file
def save_uploadedfile(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return os.path.join("uploads", uploadedfile.name)

def main():
    st.title("Chatbot3 with Transcript")

    # Create a folder to store uploaded PDFs if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Upload the PDF containing the transcript
    uploaded_file = st.file_uploader("Upload the PDF containing the transcript", type="pdf")

    if uploaded_file is not None:
        file_path = save_uploadedfile(uploaded_file)

        prompt = st.text_input("You: ", "Ask me something...")

        if st.button("Ask"):
            if prompt.lower() != 'exit' and prompt.strip() != "":
                with open(file_path, "rb") as file:
                    # Extract text from the PDF
                    pdf_reader = PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()

                prompt_with_transcript = f"""understand the transcript and have the ability to have general conversation as if i am talking to a human:

{text}

Question: {prompt}
"""
                response = model.generate_content(prompt_with_transcript)
                st.write("Bot:", response.text)

if __name__ == '__main__':
    main()