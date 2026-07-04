import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import re
from openai import OpenAI
from semantic_matcher import SemanticMatcher


st.set_page_config(
    page_title="PrepGenius AI",
    page_icon="🚀",
    layout="wide"
)


# ---------- Load Semantic Matcher (cached so it loads once, not per-click) ----------

@st.cache_resource
def load_matcher():
    return SemanticMatcher()

matcher = load_matcher()

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
        text += para.text + "\n"
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


def generate_ai_feedback(resume_text, jd_text, score, semantic_score=None, semantic_gaps=None, backend="Ollama (local)", ollama_model="llama3.2", groq_model="llama-3.1-8b-instant"):
    if backend == "Groq (cloud)":
        # Groq exposes an OpenAI-compatible endpoint, so we reuse the same
        # client -- just point it at Groq's server with a Groq API key.
        # Free key from https://console.groq.com/keys
        try:
            groq_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            raise RuntimeError(
                "GROQ_API_KEY not found. Add it to .streamlit/secrets.toml as: "
                'GROQ_API_KEY = "your-key-here"'
            )
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_key
        )
        model_name = groq_model
    else:
        # Ollama exposes an OpenAI-compatible endpoint locally, so we reuse
        # the same client -- just point it at localhost, no API key needed.
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # required by the client library, but unused by Ollama
        )
        model_name = ollama_model

    tone_instruction = """
If alignment is low, be encouraging and constructive.
Avoid negative or harsh language.
Focus on improvement, not criticism.
"""

    gaps_text = ""
    if semantic_gaps:
        gap_lines = "\n".join(f"- {g['requirement']}" for g in semantic_gaps)
        gaps_text = f"\nRequirements with weak semantic coverage in the resume:\n{gap_lines}\n"

    prompt = f"""
You are a senior technical recruiter.

Resume:
{resume_text}

Job Description:
{jd_text}

Current keyword similarity score: {score}%
Current semantic similarity score: {semantic_score}%
{gaps_text}
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
        model=model_name,
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
# NOTE: results are stored in st.session_state so they survive the rerun
# that happens when "Generate Detailed Feedback" is clicked below. Without
# this, clicking that button would reset "Run Analysis" to False and the
# whole results section (including that button) would disappear before
# the feedback could ever be generated.

if st.button("Run Analysis"):

    if not resume_text or not job_description:
        st.warning("Please provide both resume and job description.")
        st.stop()

    cleaned_resume = normalize(resume_text)
    cleaned_jd = normalize(job_description)

    score = compute_similarity(cleaned_resume, cleaned_jd)

    with st.spinner("Running semantic analysis..."):
        semantic_result = matcher.match(resume_text, job_description)
    semantic_score = semantic_result.get("overall_semantic_score", 0)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    missing_skills = jd_skills - resume_skills
    matching_skills = resume_skills.intersection(jd_skills)

    st.session_state["analysis"] = {
        "resume_text": resume_text,
        "job_description": job_description,
        "score": score,
        "semantic_score": semantic_score,
        "semantic_result": semantic_result,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }
    # Clear any previous feedback so old results don't linger for a new resume/JD pair
    st.session_state.pop("feedback", None)


# ---------- Display results (reads from session_state, survives reruns) ----------

if "analysis" in st.session_state:
    a = st.session_state["analysis"]
    score = a["score"]
    semantic_score = a["semantic_score"]
    semantic_result = a["semantic_result"]
    matching_skills = a["matching_skills"]
    missing_skills = a["missing_skills"]
    semantic_gaps = semantic_result.get("likely_skill_gaps", [])

    st.markdown("## Alignment Overview")
    st.progress(int(score))

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.markdown(
            f"<div class='metric-box'><h2>{score}%</h2><p>Keyword Match Score</p></div>",
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            f"<div class='metric-box'><h2>{semantic_score}%</h2><p>Semantic Match Score</p></div>",
            unsafe_allow_html=True
        )

    with col_c:
        st.markdown(
            f"<div class='metric-box'><h2>{len(matching_skills)}</h2><p>Matching Skills</p></div>",
            unsafe_allow_html=True
        )

    with col_d:
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

    st.markdown("## Semantic Requirement Breakdown")
    st.caption("Catches paraphrased skills that keyword matching misses (e.g. 'built REST APIs' vs 'developed backend services').")

    with st.expander("See requirement-level matches"):
        for r in semantic_result.get("requirement_matches", []):
            st.write(f"**{r['similarity']:.2f}** — {r['requirement']}")
            st.caption(f"Closest resume line: {r['best_resume_match']}")

    if semantic_gaps:
        st.subheader("Likely Skill Gaps (semantic)")
        for gap in semantic_gaps:
            st.warning(gap["requirement"])

    st.markdown("## AI Insight")

    backend_choice = st.radio(
        "Choose feedback engine",
        ["Ollama (local)", "Groq (cloud)"],
        horizontal=True,
        key="backend_choice",
        help="Ollama runs free on your machine but won't work once this app is deployed online. Groq is a free cloud API that works both locally and when deployed."
    )

    ollama_model = "llama3.2"
    groq_model = "llama-3.1-8b-instant"

    if backend_choice == "Ollama (local)":
        ollama_model = st.text_input(
            "Ollama model name",
            value="llama3.2",
            help="Must match a model you've already pulled, e.g. run 'ollama list' to check."
        )
    else:
        groq_model = st.text_input(
            "Groq model name",
            value="llama-3.1-8b-instant",
            help="Free key from https://console.groq.com/keys — add it to .streamlit/secrets.toml as GROQ_API_KEY."
        )

    if st.button("Generate Detailed Feedback"):
        with st.spinner(f"Analyzing alignment using {backend_choice}..."):
            try:
                feedback = generate_ai_feedback(
                    a["resume_text"],
                    a["job_description"],
                    score,
                    semantic_score=semantic_score,
                    semantic_gaps=semantic_gaps,
                    backend=backend_choice,
                    ollama_model=ollama_model,
                    groq_model=groq_model
                )
                st.session_state["feedback"] = feedback
            except Exception as e:
                st.error(f"Feedback generation failed: {e}")
                if backend_choice == "Ollama (local)":
                    st.info("Make sure Ollama is running ('ollama serve') and the model name matches 'ollama list'.")
                else:
                    st.info("Check that GROQ_API_KEY is set correctly in .streamlit/secrets.toml.")

    if "feedback" in st.session_state:
        st.markdown(st.session_state["feedback"])