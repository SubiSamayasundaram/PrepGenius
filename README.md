# PrepGenius

## AI Resume Intelligence Suite

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![Domain](https://img.shields.io/badge/Domain-NLP-green)
![Semantic Matching](https://img.shields.io/badge/Semantic%20Matching-Sentence%20Transformers-orange)
![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20Ollama-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview

PrepGenius is an AI-powered resume intelligence platform designed to evaluate resume–job alignment, identify technical skill gaps, and generate role-specific resume optimization feedback using Natural Language Processing and semantic similarity analysis.

The platform combines traditional keyword-based similarity scoring with transformer-based semantic matching to identify both direct keyword overlap and conceptually related experience.

By integrating Sentence-Transformer embeddings and Large Language Model-based analysis, PrepGenius provides a comprehensive assessment of resume relevance for a target job description.

---

## Core Capabilities

### 1. Resume–Job Match Analysis

- Cosine similarity scoring using vectorized text
- Keyword overlap analysis
- Resume–job alignment percentage
- Visual representation of match strength

### 2. Semantic Match Analysis

- Sentence embedding generation using Sentence-Transformers
- MiniLM-based semantic similarity analysis
- Requirement-level resume matching
- Detection of paraphrased and conceptually related experience
- Automatic identification of weak semantic matches

Each job requirement is compared with the most relevant resume statement and assigned a semantic similarity score.

Matches below a defined similarity threshold are identified as potential skill gaps.

### 3. Skill Gap Detection

- Identifies missing technical keywords
- Detects weak semantic alignment
- Separates matched and missing requirements
- Evaluates overall resume alignment strength

The system combines keyword-based and semantic gap detection to provide a more comprehensive analysis of resume–job alignment.

### 4. AI Resume Optimization

- Role-specific skill recommendations
- Resume bullet-point refinement
- Professional summary enhancement
- Achievement quantification suggestions
- ATS-oriented keyword optimization

Large Language Models are used to generate contextual optimization recommendations based on the candidate's resume and target job description.

### 5. Flexible LLM Backend

PrepGenius supports cloud-based and local Large Language Model inference.

- Groq API for cloud-based LLM inference
- Ollama for local LLM inference
- Local processing support
- Flexible LLM backend selection

The pluggable LLM architecture allows the application to use local inference as an alternative to cloud-based APIs.

### 6. Flexible Input Support

- PDF resume upload
- DOCX resume upload
- Manual text input

Uploaded documents are processed through a text extraction and normalization pipeline before analysis.

---

## Semantic Matching Evaluation

The semantic matching module improves resume–job alignment detection by identifying contextual relationships that traditional keyword matching may fail to capture.

| Matching Method | Match Score |
|---|---:|
| Keyword-Based Similarity | 32.55% |
| Semantic Similarity | 50.9% |
| Improvement | 18+ percentage points |

For example:

> **Resume:** Built REST APIs for an AI application.

> **Job Requirement:** Experience developing backend services.

Although the statements contain limited direct keyword overlap, semantic matching identifies their conceptual relationship.

---

## System Architecture

```text
User Input (PDF / DOCX / Text)
              |
              v
       Text Extraction
              |
              v
      Text Normalization
              |
              v
      Keyword Vectorization
       (CountVectorizer)
              |
              v
   Cosine Similarity Analysis
              |
              v
 Semantic Embedding Generation
   (Sentence-Transformers)
              |
              v
 Requirement-Level Matching
              |
       +------+------+
       |             |
       v             v
 Keyword Gap    Semantic Gap
   Detection      Detection
       |             |
       +------+------+
              |
              v
    Hybrid Skill Gap Analysis
              |
              v
     LLM-Based Optimization
              |
       +------+------+
       |             |
       v             v
    Groq API       Ollama
              |
              v
 Resume Intelligence Dashboard
```

---

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- Sentence-Transformers
- MiniLM
- PyPDF2
- python-docx
- Groq API
- Ollama

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SubiSamayasundaram/PrepGenius.git
cd PrepGenius
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

> LLM-based resume optimization supports Groq API and Ollama backends. Configure the preferred backend before using AI optimization features.

---

## Future Enhancements

- Weighted hybrid lexical and semantic scoring
- Named Entity Recognition for structured skill extraction
- Resume section-level analysis
- Experience relevance scoring
- Advanced ATS compatibility analysis
- Multi-job description comparison
- Automatic target-role classification
- Vector database integration
- Recruiter-oriented analytics dashboard

---

## Author

**Subi Samayasundaram**

B.Tech Artificial Intelligence and Machine Learning  
St. Joseph's College of Engineering

Areas of interest include Generative AI, Natural Language Processing, Large Language Models, Machine Learning, and intelligent AI systems.

---

## License

This project is licensed under the MIT License.
