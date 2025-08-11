# src/rag_engine.py
"""
Local RAG engine for ADGM Corporate Agent.

Behavior:
- Loads plaintext reference files from ./legal_refs/*.txt
- If scikit-learn available, builds TF-IDF + cosine similarity index to find best-matching snippets
- Returns a short citation string and a float confidence score (0.0-1.0)
- Falls back to STATIC_RULES when no refs or sklearn not available
"""

import os
import glob
import logging
from typing import Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STATIC_RULES = {
    "jurisdiction": "ADGM Companies Regulations 2020, Part 3, Section 15 — Jurisdiction must be ADGM Courts.",
    "signature": "ADGM Companies Regulations 2020, Schedule 1 — Documents must be signed by an authorised signatory.",
    "ambiguous": "ADGM Guidance on Contract Drafting — Avoid non-binding terms such as 'may' or 'endeavour'.",
    "numbered clauses": "ADGM Best Practice Templates — Use numbered clauses for clarity."
}

# reference dir (create folder ./legal_refs and place .txt files there)
REF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "legal_refs"))

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

class LocalRAG:
    def __init__(self, ref_dir=REF_DIR):
        self.ref_dir = ref_dir
        self.docs = []          # full text per file
        self.doc_names = []     # filenames
        self.vectorizer = None
        self.doc_vectors = None
        self.use_sklearn = SKLEARN_AVAILABLE
        self._load_refs()

    def _load_refs(self):
        if not os.path.isdir(self.ref_dir):
            logger.info("RAG: ref dir not found (%s). Using STATIC_RULES fallback.", self.ref_dir)
            return

        files = sorted(glob.glob(os.path.join(self.ref_dir, "*.txt")))
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    txt = fh.read().strip()
                    if txt:
                        self.docs.append(txt)
                        self.doc_names.append(os.path.basename(f))
            except Exception as e:
                logger.exception("RAG: failed to read ref file %s: %s", f, e)

        if not self.docs:
            logger.info("RAG: no text files loaded from %s", self.ref_dir)
            self.use_sklearn = False
            return

        if self.use_sklearn:
            try:
                self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
                self.doc_vectors = self.vectorizer.fit_transform(self.docs)
                logger.info("RAG: TF-IDF index built with %d documents", len(self.docs))
            except Exception as e:
                logger.exception("RAG: sklearn TF-IDF build failed: %s", e)
                self.use_sklearn = False

    def query(self, q: str, top_k: int = 1) -> Tuple[str, float]:
        """
        Query RAG with text `q`.
        Returns (citation_text, score) where score in [0.0, 1.0].
        If low confidence or fallback, returns STATIC_RULE (ambiguous) or matching static rule.
        """
        if not q:
            return "", 0.0

        q_low = q.lower()

        # quick keyword -> static map
        for key, text in STATIC_RULES.items():
            if key in q_low:
                # exact static hit gets full confidence
                return f"STATIC_RULE — {text}", 1.0

        # if we have vectors, do semantic search
        if self.use_sklearn and self.doc_vectors is not None and self.docs:
            try:
                q_vec = self.vectorizer.transform([q])
                sims = cosine_similarity(q_vec, self.doc_vectors)[0]
                top_idx = int(sims.argmax())
                score = float(sims[top_idx])
                # apply threshold
                if score < 0.08:
                    # low confidence - return the ambiguous STATIC_RULE
                    return f"STATIC_RULE — {STATIC_RULES.get('ambiguous','')}", 0.0
                name = self.doc_names[top_idx]
                excerpt = self.docs[top_idx][:600].replace("\n", " ").strip()
                citation = f"{name} — {excerpt}..."
                # normalize score (sims are already 0-1-ish for cosine; keep as is)
                return citation, float(round(score, 3))
            except Exception as e:
                logger.exception("RAG: query failed: %s", e)
                return f"STATIC_RULE — {STATIC_RULES.get('ambiguous','')}", 0.0

        # fallback: return ambiguous static rule
        return f"STATIC_RULE — {STATIC_RULES.get('ambiguous','')}", 0.0

    def citation_for_docname(self, doc_name: str) -> Tuple[str, float]:
        """
        Try to match a document name (e.g., 'UBO Declaration Form') to loaded ref files.
        """
        if not doc_name:
            return "", 0.0
        name = doc_name.lower()
        # exact / prefix or substring match in filenames
        for i, fname in enumerate(self.doc_names):
            if fname.lower().startswith(name) or name in fname.lower():
                excerpt = self.docs[i][:600].replace("\n", " ").strip()
                return f"{fname} — {excerpt}...", 1.0
        # fallback try static rules
        for key, text in STATIC_RULES.items():
            if key in name:
                return f"STATIC_RULE — {text}", 1.0
        return f"STATIC_RULE — {STATIC_RULES.get('ambiguous','')}", 0.0

# single instance
_rag = LocalRAG()

def get_legal_reference(query: str) -> str:
    """
    Convenience wrapper returns a human-readable text including score.
    Example: "myfile.txt — excerpt... (score=0.72)"
    """
    try:
        citation, score = _rag.query(query)
        if not citation:
            return ""
        # append score for debugging / visibility
        return f"{citation} (score={score})"
    except Exception:
        return STATIC_RULES.get("ambiguous", "")

def get_citation_for_docname(doc_name: str) -> str:
    try:
        citation, score = _rag.citation_for_docname(doc_name)
        if not citation:
            return ""
        return f"{citation} (score={score})"
    except Exception:
        return ""
