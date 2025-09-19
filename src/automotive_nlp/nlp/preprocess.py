import spacy
from typing import Optional

# load small model; in a production environment you may prefer a larger model or a sentence transformer
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    # If the model isn't installed, raise helpful error
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm"
    )

def clean_text(text: str) -> str:
    if not text:
        return ""
    doc = nlp(text.lower())
    tokens = [t.lemma_ for t in doc if not t.is_stop and t.is_alpha]
    return " ".join(tokens)
