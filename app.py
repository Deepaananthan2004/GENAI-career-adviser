import streamlit as st
import os
import fitz  # PyMuPDF
import spacy
import spacy.cli
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Safe spaCy model loading
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.info("Downloading 'en_core_web_sm' model. Please wait...")
    os.system("python -m spacy download en_core_web_sm --user")
    nlp = spacy.load("en_core_web_sm")

# Initialize Groq client
GROK_API_KEY = os.getenv("GROQ_API_KEY")
if not GROK_API_KEY:
    st.error("GROQ_API_KEY not found in environment variables.")
    st.stop()

client = Groq(api_key=GROK_API_KEY)

def chat_with_grok(prompt):
    try:
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
    except Exception as e:
        return f"Error communicating with Groq API: {e}"

def extract_pdf_skills_experience(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        doc_nlp = nlp(text)

        skills = [ent.text for ent in doc_nlp.ents if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART"]]
        experience = [
            sent.text for sent in doc_nlp.sents
            if "intern" in sent.text.lower() or "experience" in sent.text.lower()
        ]
        return skills, experience
    except Exception as e:
        return [], [f"Error reading PDF: {e}"]

st.set_page_config(page_title="AI Career Adviser", layout="centered")
st.title("AI Career Adviser with Groq API and Resume Analyzer")

st.write("Get personalized career advice or upload your resume for automatic skill and experience extraction.")

prompt = st.text_input("Ask Groq something about careers or resumes:")
if prompt:
    with st.spinner("Getting advice from Groq..."):
        reply = chat_with_grok(prompt)
    st.subheader("Grok Reply:")
    st.write(reply)

uploaded_pdf = st.file_uploader("Upload your resume (PDF):", type=["pdf"])
if uploaded_pdf is not None:
    st.info("Extracting details from your resume...")
    skills, experience = extract_pdf_skills_experience(uploaded_pdf)

    st.subheader("Extracted Skills:")
    st.write(skills if skills else "No clear skills detected.")

    st.subheader("Extracted Experience:")
    st.write(experience if experience else "No experience details found.")

st.markdown("---")
st.caption("Built using Streamlit, spaCy, Groq API, and PyMuPDF.")
