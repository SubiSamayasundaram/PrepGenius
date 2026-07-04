
from sentence_transformers import SentenceTransformer, util
import re
from typing import List, Dict


class SemanticMatcher:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        all-MiniLM-L6-v2: distilled BERT-family model, 384-dim embeddings,
        fast enough to run on CPU (important for a Streamlit demo with no GPU).
        Swap to 'distilbert-base-nli-stsb-mean-tokens' if you specifically
        want to say "DistilBERT" on your resume (slightly slower, ~5-10s/query).
        """
        self.model = SentenceTransformer(model_name)

    def _chunk_resume(self, resume_text: str) -> List[str]:
        """
        Split resume into bullet/section-level chunks for granular matching.
        PDF extraction often strips newlines and flattens the whole resume
        into one dense line with little punctuation (e.g. "TECHNICAL SKILLS
        Languages: Python..."). To handle this, insert breaks before likely
        section boundaries -- ALL-CAPS header runs and year markers -- in
        addition to normal newline/sentence splitting.
        """
        text = resume_text

        # Break before ALL-CAPS header runs (e.g. "TECHNICAL SKILLS", "PROJECTS")
        text = re.sub(r'(?<=[a-z0-9\.,\)])\s+(?=[A-Z]{2,}(?:\s[A-Z]{2,}){0,3}\b)', '\n', text)

        # Break before 4-digit years (job/project entries usually start near a year)
        text = re.sub(r'\s+(?=(19|20)\d{2}\b)', '\n', text)

        # Break before pipe-separated header fields (common in resume contact lines)
        text = text.replace(" | ", "\n")

        lines = [l.strip("•-* \t") for l in text.split("\n")]
        lines = [l for l in lines if len(l.split()) > 3]

        # Fallback: if still collapsed into one giant chunk, split on sentences
        if len(lines) <= 1:
            sentences = re.split(r'(?<=[.!?])\s+', resume_text)
            lines = [s.strip("•-* \t") for s in sentences if len(s.split()) > 3]

        return lines

    def _chunk_jd(self, jd_text: str) -> List[str]:
        """Split JD into requirement-level sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', jd_text)
        return [s.strip() for s in sentences if len(s.split()) > 3]

    def match(self, resume_text: str, jd_text: str, top_k: int = 5) -> Dict:
        """
        Computes:
        1. Overall semantic similarity score (0-100) between full resume and JD.
        2. Per-requirement matching: for each JD requirement, finds the best
           matching resume bullet and its similarity score.
        3. Unmatched requirements (potential skill gaps), sorted by how far
           they are from anything in the resume.
        """
        resume_chunks = self._chunk_resume(resume_text)
        jd_chunks = self._chunk_jd(jd_text)

        if not resume_chunks or not jd_chunks:
            return {"error": "Could not extract enough text to compare."}

        resume_embeds = self.model.encode(resume_chunks, convert_to_tensor=True)
        jd_embeds = self.model.encode(jd_chunks, convert_to_tensor=True)

        # Overall score: mean of full-document embeddings
        overall_resume_embed = self.model.encode(resume_text, convert_to_tensor=True)
        overall_jd_embed = self.model.encode(jd_text, convert_to_tensor=True)
        overall_score = util.cos_sim(overall_resume_embed, overall_jd_embed).item()

        # Per-requirement best match
        sim_matrix = util.cos_sim(jd_embeds, resume_embeds)  # [jd_chunks x resume_chunks]

        requirement_matches = []
        for i, jd_line in enumerate(jd_chunks):
            best_idx = sim_matrix[i].argmax().item()
            best_score = sim_matrix[i][best_idx].item()
            requirement_matches.append({
                "requirement": jd_line,
                "best_resume_match": resume_chunks[best_idx],
                "similarity": round(best_score, 3)
            })

        # Sort to surface weakest matches first (likely skill gaps)
        requirement_matches.sort(key=lambda x: x["similarity"])
        gaps = [r for r in requirement_matches if r["similarity"] < 0.30][:top_k]

        return {
            "overall_semantic_score": round(overall_score * 100, 1),
            "requirement_matches": requirement_matches,
            "likely_skill_gaps": gaps
        }


# ---------------------------------------------------------------------------
# Quick standalone test / demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_resume = """
    Built REST APIs using Flask and deployed on AWS EC2.
    Developed a machine learning pipeline for churn prediction using scikit-learn.
    Wrote unit tests and set up CI/CD with GitHub Actions.
    Collaborated with cross-functional teams on data pipeline design.
    """

    sample_jd = """
    We are looking for a backend engineer experienced in building scalable web services.
    Familiarity with cloud deployment (AWS or GCP) is required.
    Experience with containerization using Docker and Kubernetes is a plus.
    Strong understanding of CI/CD practices is expected.
    Experience with NLP or LLM-based systems is a bonus.
    """

    matcher = SemanticMatcher()
    result = matcher.match(sample_resume, sample_jd)

    print(f"\nOverall Semantic Match Score: {result['overall_semantic_score']}%\n")
    print("Requirement-level matches (weakest first):")
    for r in result["requirement_matches"]:
        print(f"  [{r['similarity']:.2f}] {r['requirement'][:60]}")
        print(f"         -> best match: {r['best_resume_match'][:60]}")

    print("\nLikely skill gaps (score < 0.35):")
    for g in result["likely_skill_gaps"]:
        print(f"  - {g['requirement']}")