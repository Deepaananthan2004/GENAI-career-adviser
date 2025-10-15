import streamlit as st
import os
import fitz  # PyMuPDF
import spacy
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Download model if not present
spacy.cli.download("en_core_web_sm")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Grok client
GROK_API_KEY = os.getenv("GROQ_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROK_API_KEY)

def chat_with_grok(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful AI career adviser."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def extract_pdf_skills_experience(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc_nlp = nlp(text)
    skills = [ent.text for ent in doc_nlp.ents if ent.label_ == "SKILL"]
    experience = [
        sent.text for sent in doc_nlp.sents
        if "intern" in sent.text.lower() or "experience" in sent.text.lower()
    ]
    return skills, experience

# Streamlit UI starts here
st.title("AI Career Adviser with Grok API and PDF Parsing")

prompt = st.text_input("Ask Grok something about careers or resumes:")
if prompt:
    reply = chat_with_grok(prompt)
    st.write("Grok Reply:")
    st.write(reply)

uploaded_pdf = st.file_uploader("Upload your resume (PDF):", type=["pdf"])
if uploaded_pdf is not None:
    skills, experience = extract_pdf_skills_experience(uploaded_pdf)
    st.write("Extracted Skills:", skills)

    st.write("Extracted Experience:", experience)
