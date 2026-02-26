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

# ---------- Minimal Premium Styling ----------

st.markdown("""
<style>
body { background-color: #0e1117; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { color: white; }
.stTextArea textarea {
    background-color: #1c1f26 !important;
    color: white !important;
}
.stButton>button {
    background: linear-gradient(90deg, #4b6cb7, #182848);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    height: 3em;
    width: 100%;
}
.metric-box {
    background: #1c1f26;
    padding: 18px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ---------- Skill Knowledge Base ----------

TECH_SKILLS = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy",
    "nlp", "computer vision",
    "docker", "kubernetes",
    "aws", "gcp", "azure",
    "rest api", "fastapi",
    "data science", "data analysis",
    "transformers", "llm", "huggingface"
]


# ---------- Utility Functions ----------

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
    vectorizer = CountVectorizer(stop_words="english").fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectorizer)[0][1]
    return round(score * 100, 2)


def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found.append(skill)
    return set(found)


def generate_ai_feedback(resume_text, jd_text, score):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    tone_instruction = """
If alignment is low, be encouraging and constructive.
Avoid negative or harsh language.
Focus on improvement, not criticism.
"""

    prompt = f"""
You are a senior technical recruiter.

Resume:
{resume_text}

Job Description:
{jd_text}

Current similarity score: {score}%

Provide structured analysis:

1. Technical alignment assessment
2. Missing or underrepresented skills
3. Experience depth evaluation
4. Practical improvement recommendations
5. Refined summary tailored to the role

{tone_instruction}

Be specific, analytical, and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content


# ---------- UI ----------

st.title("PrepGenius – AI Resume Intelligence Suite")
st.markdown("Resume–Job Alignment • Skill Gap Analysis • AI Optimization")

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


# ---------- Analysis ----------

if st.button("Run Analysis"):

    if not resume_text or not job_description:
        st.warning("Please provide both resume and job description.")
        st.stop()

    cleaned_resume = normalize(resume_text)
    cleaned_jd = normalize(job_description)

    score = compute_similarity(cleaned_resume, cleaned_jd)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    missing_skills = jd_skills - resume_skills
    matching_skills = resume_skills.intersection(jd_skills)

    st.markdown("## Alignment Overview")
    st.progress(int(score))

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            f"<div class='metric-box'><h2>{score}%</h2><p>Match Score</p></div>",
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            f"<div class='metric-box'><h2>{len(matching_skills)}</h2><p>Matching Skills</p></div>",
            unsafe_allow_html=True
        )

    with col_c:
        st.markdown(
            f"<div class='metric-box'><h2>{len(missing_skills)}</h2><p>Skill Gaps</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("## Skill Alignment")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Aligned Skills")
        if matching_skills:
            st.write(sorted(list(matching_skills)))
        else:
            st.write("No strong technical overlap detected yet.")

    with col_right:
        st.subheader("Areas to Strengthen")
        if missing_skills:
            st.write(sorted(list(missing_skills)))
        else:
            st.success("Core technical requirements appear aligned.")

    st.markdown("## AI Insight")

    if st.button("Generate Detailed Feedback"):
        with st.spinner("Analyzing alignment..."):
            feedback = generate_ai_feedback(resume_text, job_description, score)
            st.markdown(feedback)
