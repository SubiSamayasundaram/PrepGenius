import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import re
from openai import OpenAI


st.set_page_config(
    page_title="PrepGenius AI",
    page_icon="🚀",
    layout="wide"
)


st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: white;
}
.stTextArea textarea {
    background-color: #1c1f26 !important;
    color: white !important;
}
.stButton>button {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white;
    border-radius: 10px;
    font-weight: 600;
    height: 3em;
    width: 100%;
}
.metric-box {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


def extract_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text


def extract_docx(file):
    document = docx.Document(file)
    text = ""
    for para in document.paragraphs:
        text += para.text + " "
    return text


def normalize(text):
    return re.sub(r"\W+", " ", text.lower())


def compute_similarity(resume_text, jd_text):
    vectorizer = CountVectorizer().fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectorizer)[0][1]
    return round(score * 100, 2)


def generate_ai_feedback(resume_text, jd_text):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
You are a senior technical recruiter and resume optimization specialist.

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Provide structured feedback in clear sections:

1. Missing technical skills relevant to this role
2. Three rewritten resume bullet points aligned with the job
3. A refined professional summary tailored to this position
4. Suggestions to quantify achievements
5. ATS optimization improvements

Be specific, role-aligned, and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


st.title("PrepGenius – AI Resume Intelligence Suite")
st.markdown("Advanced Resume Analysis • Skill Gap Detection • AI Optimization")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    resume_text = ""

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_pdf(uploaded_file)
        else:
            resume_text = extract_docx(uploaded_file)

    manual_resume = st.text_area("Or paste resume content")

    if manual_resume:
        resume_text = manual_resume


with col2:
    st.subheader("Job Description")
    job_description = st.text_area("Paste job description")


if st.button("Run Analysis"):

    if not resume_text or not job_description:
        st.warning("Please provide both resume and job description.")
        st.stop()

    cleaned_resume = normalize(resume_text)
    cleaned_jd = normalize(job_description)

    score = compute_similarity(cleaned_resume, cleaned_jd)

    st.markdown("## Match Score")
    st.progress(int(score))

    col_a, col_b, col_c = st.columns(3)

    job_words = set(cleaned_jd.split())
    resume_words = set(cleaned_resume.split())
    missing_keywords = list(job_words - resume_words)[:15]
    matching_keywords = len(resume_words.intersection(job_words))

    with col_a:
        st.markdown(
            f"<div class='metric-box'><h2>{score}%</h2><p>Overall Match</p></div>",
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            f"<div class='metric-box'><h2>{len(missing_keywords)}</h2><p>Missing Keywords</p></div>",
            unsafe_allow_html=True
        )

    with col_c:
        st.markdown(
            f"<div class='metric-box'><h2>{matching_keywords}</h2><p>Matching Keywords</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("## Identified Skill Gaps")
    if missing_keywords:
        st.write(missing_keywords)
    else:
        st.success("No major keyword gaps detected.")

    st.markdown("## AI Optimization Feedback")

    if st.button("Generate AI Suggestions"):
        with st.spinner("Generating detailed feedback..."):
            feedback = generate_ai_feedback(resume_text, job_description)
            st.markdown(feedback)
