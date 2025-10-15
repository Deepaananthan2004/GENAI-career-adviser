import fitz
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    experience = [sent.text for sent in doc.sents if "intern" in sent.text.lower() or "experience" in sent.text.lower()]
    
    return {"skills": skills, "experience": experience}