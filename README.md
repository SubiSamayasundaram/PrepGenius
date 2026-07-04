PrepGenius
AI Resume Intelligence Suite

Overview
PrepGenius is an AI-powered resume intelligence platform designed to evaluate resume–job alignment, detect technical skill gaps, and generate role-specific optimization feedback using NLP, semantic similarity, and GPT-based analysis.
It combines keyword-based similarity scoring with BERT-based semantic matching (via sentence-transformers) to capture not just exact keyword overlap but paraphrased and conceptually related skills, helping candidates tailor their resumes for specific job descriptions with greater accuracy.

Core Capabilities
1. Resume–Job Match Analysis

* Cosine similarity scoring using vectorized text
* Keyword overlap detection
* Match percentage with visual indicators

1b. Semantic Match Analysis (BERT-based)

* Upgrades keyword-based cosine similarity with BERT sentence embeddings (sentence-transformers, MiniLM)
* Captures paraphrased skills that exact keyword matching misses (e.g. "built REST APIs" vs "developed backend services")
* Requirement-level breakdown: each job requirement is matched against its closest resume line, with a similarity score
* Automatically flags weak semantic matches (score < 0.30) as likely skill gaps
* Result on real resume/JD test: improved match detection by 18+ points (32.55% keyword → 50.9% semantic)

2. Skill Gap Detection

* Identifies missing technical keywords
* Displays matching vs missing terms
* Highlights resume alignment strength

3. AI Resume Optimization

* Role-specific missing skill recommendations
* Resume bullet rewriting aligned to job description
* Professional summary refinement
* Achievement quantification suggestions
* ATS keyword optimization improvements
* Pluggable LLM backend: supports both cloud (OpenAI GPT-4o-mini) and local (Ollama) inference, allowing cost-free offline operation as a fallback

4. Flexible Input Support

* Upload PDF resumes
* Upload DOCX resumes
* Manual text input

System Architecture
User Input (PDF/DOCX/Text) → Text Extraction → Text Normalization → Vectorization (CountVectorizer) → Cosine Similarity Scoring → Semantic Embedding Matching (BERT) → Keyword Gap Detection → Semantic Gap Detection → GPT/Ollama-Based Optimization Feedback

Technology Stack

* Python
* Streamlit
* Scikit-learn
* PyPDF2
* python-docx
* OpenAI API
* Sentence-Transformers (BERT/MiniLM embeddings)
* Ollama (optional local LLM backend)

Installation
Clone the repository:

```
git clone https://github.com/SubiSamayasundaram/PrepGenius.git
cd PrepGenius
```

Install dependencies:

```
pip install -r requirements.txt
```

Set up your OpenAI API key (only needed if using the OpenAI backend):

```
mkdir .streamlit
echo OPENAI_API_KEY = "your-key-here" > .streamlit/secrets.toml
```

Or, to use the local Ollama backend instead (no API key required):

```
ollama pull llama3
ollama serve
```

Run the app:

```
streamlit run app.py
```