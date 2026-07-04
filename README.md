# PrepGenius  
### AI Resume Intelligence Suite

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![NLP](https://img.shields.io/badge/Domain-NLP-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview

PrepGenius is an AI-powered resume intelligence platform designed to evaluate resume–job alignment, detect technical skill gaps, and generate role-specific optimization feedback using NLP and GPT-based analysis.

It combines traditional keyword similarity scoring with AI-driven refinement to help candidates tailor their resumes for specific job descriptions.

---

## Core Capabilities

### 1. Resume–Job Match Analysis

- Cosine similarity scoring using vectorized text
- Keyword overlap detection
- Match percentage with visual indicators

### 2. Skill Gap Detection

- Identifies missing technical keywords
- Displays matching vs missing terms
- Highlights resume alignment strength

### 3. AI Resume Optimization

- Role-specific missing skill recommendations
- Resume bullet rewriting aligned to job description
- Professional summary refinement
- Achievement quantification suggestions
- ATS keyword optimization improvements

### 4. Flexible Input Support

- Upload PDF resumes
- Upload DOCX resumes
- Manual text input

---

## System Architecture


User Input (PDF/DOCX/Text)
↓
Text Extraction
↓
Text Normalization
↓
Vectorization (CountVectorizer)
↓
Cosine Similarity Scoring
↓
Keyword Gap Detection
↓
GPT-Based Optimization Feedback


---

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- PyPDF2
- python-docx
- OpenAI API

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SubiSamayasundaram/PrepGenius.git
cd PrepGenius
