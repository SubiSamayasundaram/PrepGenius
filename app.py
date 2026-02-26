import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import re

st.set_page_config(page_title="PrepGenius", page_icon="🚀", layout="wide")

# ------------------ FUNCTIONS ------------------

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    return text.lower()

def calculate_similarity(resume, job_desc):
    vectorizer = CountVectorizer().fit_transform([resume, job_desc])
    similarity = cosine_similarity(vectorizer)[0][1]
    return round(similarity * 100, 2)

# ------------------ UI ------------------

st.title("🚀 PrepGenius – AI Interview Toolkit")
st.markdown("### Smart Resume Analysis & Skill Gap Detection")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    
    resume_text = ""
    
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)

    resume_manual = st.text_area("Or Paste Resume Text")

    if resume_manual:
        resume_text = resume_manual

with col2:
    st.subheader("📌 Job Description")
    job_desc = st.text_area("Paste Job Description")

# ------------------ ANALYSIS ------------------

if st.button("🔍 Analyze Resume"):
    
    if resume_text and job_desc:
        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        score = calculate_similarity(resume_clean, job_clean)

        st.markdown("## 📊 Match Analysis")
        st.progress(int(score))

        if score > 70:
            st.success(f"Excellent Match: {score}% 🎯")
        elif score > 40:
            st.warning(f"Moderate Match: {score}% ⚡")
        else:
            st.error(f"Low Match: {score}% ❌")

        # Skill Gap Detection
        job_words = set(job_clean.split())
        resume_words = set(resume_clean.split())
        missing_skills = job_words - resume_words

        st.markdown("## 🧠 Missing Skills (Based on JD)")
        if missing_skills:
            st.write(list(missing_skills)[:10])
        else:
            st.success("No major missing keywords detected!")

        # Suggestions
        st.markdown("## 💡 Suggestions to Improve")
        st.write("• Add more project-specific keywords from the job description.")
        st.write("• Include measurable achievements (e.g., improved model accuracy by 15%).")
        st.write("• Highlight relevant tools & technologies.")
        st.write("• Customize resume summary for this role.")

    else:
        st.warning("Please upload/paste resume and job description.")
