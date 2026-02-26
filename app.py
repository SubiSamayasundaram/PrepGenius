import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🚀 PrepGenius – AI Interview Toolkit")

st.header("📄 Resume Analyzer")

resume = st.text_area("Paste Your Resume")
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze Match"):
    vectorizer = CountVectorizer().fit_transform([resume, job_desc])
    similarity = cosine_similarity(vectorizer)[0][1]
    score = round(similarity * 100, 2)
    st.success(f"Match Score: {score}%")
