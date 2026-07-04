<div align="center">

# 🚀 PrepGenius

### AI Resume Intelligence Suite

**Analyze Resume–Job Alignment • Detect Skill Gaps • Optimize with AI**

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![NLP](https://img.shields.io/badge/Domain-NLP-green)
![Semantic AI](https://img.shields.io/badge/Semantic%20AI-MiniLM-orange)
![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20Ollama-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

<br>

> **A hybrid NLP and semantic intelligence platform designed to evaluate resume relevance beyond traditional keyword matching.**

</div>

---

## 📌 Overview

**PrepGenius** is an AI-powered resume intelligence platform designed to evaluate **resume–job alignment**, identify **technical skill gaps**, and generate **role-specific resume optimization feedback**.

The platform combines traditional keyword-based similarity analysis with transformer-based semantic matching to identify both direct keyword overlap and conceptually related experience.

By integrating **Sentence-Transformer embeddings**, **MiniLM-based semantic similarity**, and **Large Language Models**, PrepGenius provides a comprehensive assessment of resume relevance for a target job description.

---

## 💡 What Makes PrepGenius Different?

Traditional resume matching systems primarily depend on exact keyword overlap.

PrepGenius combines:

| Approach | Purpose |
|---|---|
| 🔍 Keyword Matching | Identifies direct terminology overlap |
| 🧠 Semantic Matching | Detects conceptually related experience |
| 📊 Skill Gap Analysis | Identifies weak or missing requirements |
| 🤖 LLM Optimization | Generates contextual resume improvements |

### Example

> **Resume:** Built REST APIs for an AI application.

> **Job Requirement:** Experience developing backend services.

A traditional keyword matcher may identify limited overlap.

**PrepGenius uses semantic embeddings to recognize the conceptual relationship between both statements.**

---

## 🧠 Core Capabilities

### 📊 1. Resume–Job Match Analysis

- Cosine similarity scoring using vectorized text
- Keyword overlap analysis
- Resume–job alignment percentage
- Visual representation of match strength

### 🔗 2. Semantic Match Analysis

- Sentence embedding generation using Sentence-Transformers
- MiniLM-based semantic similarity analysis
- Requirement-level resume matching
- Detection of paraphrased experience
- Identification of conceptually related technical skills
- Automatic detection of weak semantic matches

Each job requirement is compared with the most relevant resume statement and assigned a semantic similarity score.

Matches below the defined similarity threshold are identified as potential skill gaps.

### 🎯 3. Skill Gap Detection

- Identifies missing technical keywords
- Detects weak semantic alignment
- Separates matched and missing requirements
- Evaluates resume alignment strength
- Highlights potential technical skill gaps

The system combines **keyword-based gap detection** and **semantic gap detection** to provide a more comprehensive assessment of resume–job alignment.

### 🤖 4. AI Resume Optimization

- Role-specific skill recommendations
- Resume bullet-point refinement
- Professional summary enhancement
- Achievement quantification suggestions
- ATS-oriented keyword optimization

Large Language Models are used to generate contextual optimization recommendations based on the candidate's resume and target job description.

### ⚡ 5. Flexible LLM Backend

PrepGenius supports both cloud-based and local Large Language Model inference.

- ⚡ **Groq API** — Cloud-based LLM inference
- 🖥️ **Ollama** — Local LLM inference
- 🔄 Flexible backend selection
- 🔐 Local processing support

The pluggable LLM architecture allows local inference to be used as an alternative to cloud-based APIs.

## 📈 Semantic Matching Evaluation

The semantic matching module improves resume–job alignment detection by identifying contextual relationships that traditional keyword matching may fail to capture.

| Matching Method | Match Score |
|---|---:|
| 🔍 Keyword-Based Similarity | 32.55% |
| 🧠 Semantic Similarity | **50.9%** |
| 📈 Improvement | **18+ percentage points** |

> Semantic matching identified relevant resume experience that was not captured through direct keyword comparison.

---

## 🏗️ System Architecture

```text
Resume / Job Description
          │
          ▼
    Text Extraction
          │
          ▼
   Text Normalization
          │
          ▼
  ┌───────┴────────┐
  │                │
  ▼                ▼
Keyword         Semantic
Matching        Matching
  │                │
  ▼                ▼
Cosine          MiniLM
Similarity      Embeddings
  │                │
  └───────┬────────┘
          │
          ▼
 Hybrid Gap Detection
          │
          ▼
  LLM Optimization
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
 Groq API     Ollama
    │           │
    └─────┬─────┘
          │
          ▼
Resume Intelligence Dashboard
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
|  Python | Core application development |
|  Streamlit | Interactive web interface |
|  Scikit-learn | Vectorization and cosine similarity |
|  Sentence-Transformers | Semantic embedding generation |
|  MiniLM | Transformer-based sentence representation |
|  PyPDF2 | PDF text extraction |
|  python-docx | DOCX document processing |
|  Groq API | Cloud-based LLM inference |
|  Ollama | Local LLM inference |

---

## 🚀 Installation

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

> **Note:** LLM-based resume optimization supports Groq API and Ollama backends. Configure the preferred backend before using AI optimization features.

---


## 📜 License

This project is licensed under the **MIT License**.

---
