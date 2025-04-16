import fitz  # PyMuPDF
import spacy
import re
import os
from docx import Document

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# ---------------------------------------
# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# ---------------------------------------
# Extract candidate's name and email
def extract_name_email(text):
    name = None
    email = None

    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            name = line.strip()
            break

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group(0)

    return name, email

# ---------------------------------------
# Extract keywords from job description
def extract_job_keywords(job_description_text):
    doc = nlp(job_description_text.lower())
    keywords = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if len(phrase.split()) <= 3:  # Ignore long chunks
            keywords.add(phrase)

    return keywords

# ---------------------------------------
# Match skills from resume
def extract_skills(text, job_keywords):
    text = text.lower()
    found_skills = set()

    for keyword in job_keywords:
        if keyword.lower() in text:
            found_skills.add(keyword.lower())
    return found_skills

# ---------------------------------------
# Analyze resume
def analyze_resume(resume_path, job_keywords):
    ext = os.path.splitext(resume_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(resume_path)
    elif ext == ".docx":
        text = extract_text_from_docx(resume_path)
    else:
        print("❌ Unsupported file format.")
        return

    name, email = extract_name_email(text)
    matched_skills = extract_skills(text, job_keywords)
    missing_skills = set(map(str.lower, job_keywords)) - matched_skills
    score = len(matched_skills) / len(job_keywords) * 100 if job_keywords else 0

    print("\n======= RESUME ANALYSIS REPORT =======")
    print(f"👤 Name           : {name if name else 'N/A'}")
    print(f"📧 Email          : {email if email else 'N/A'}")
    print(f"✅ Matched Skills : {', '.join(matched_skills) if matched_skills else 'None'}")
    print(f"❌ Missing Skills : {', '.join(missing_skills) if missing_skills else 'None'}")
    print(f"📊 Match Score    : {score:.2f}%")
    print("======================================\n")

# ---------------------------------------
# Main script
if __name__ == "__main__":
    # Load job description text
    try:
        with open("DESCRIPTION.txt", "r", encoding="utf-8") as f:
            jd_text = f.read()
    except FileNotFoundError:
        print("❌ job_description.txt not found.")
        exit()

    job_keywords = extract_job_keywords(jd_text)
    print(f"\n🧠 Extracted Job Keywords ({len(job_keywords)}):\n{job_keywords}\n")

    # Set your resume file here (PDF or DOCX)
    resume_file = "C:/Users/vijay kumar/OneDrive/Desktop/MURGESHAN KEERTHI.pdf"
    if not os.path.exists(resume_file):
        print(f"❌ Resume file not found: {resume_file}")
        exit()

    analyze_resume(resume_file, job_keywords)
