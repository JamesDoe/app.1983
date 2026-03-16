from __future__ import annotations

import re
import string
from collections import defaultdict
from datetime import datetime

import polars as pl
import spacy

from csg.config import DEFAULT_CONFIG
from csg.extract.normalize import normalize_text


REGIONAL_TERMS = {"hrbt", "vb", "odu", "norfolk", "ghent"}
KEEP_SINGLE_TOKEN_PHRASES = {
    "abortion",
    "democrats",
    "epstein",
    "ghent",
    "hrbt",
    "ice",
    "immigration",
    "norfolk",
    "odu",
    "texas",
    "trump",
    "vb",
}
GENERIC_TOKENS = {
    "100",
    "absolutely",
    "actually",
    "arent",
    "believe",
    "bot",
    "calm",
    "clear",
    "common",
    "come",
    "cool",
    "course",
    "day",
    "deflection",
    "disagree",
    "exactly",
    "good",
    "got",
    "haha",
    "haters",
    "im",
    "idea",
    "just",
    "maybe",
    "mean",
    "nice",
    "oh",
    "period",
    "point",
    "problem",
    "seriously",
    "sharing",
    "sorry",
    "stop",
    "sure",
    "tell",
    "thats",
    "theyre",
    "try",
    "welcome",
    "youre",
}
EXCLUDED_PHRASES = {
    "agree",
    "agreed",
    "aren t",
    "common sense",
    "correct",
    "didn t",
    "dont",
    "fuck",
    "good",
    "know",
    "like",
    "lmao",
    "lol",
    "look",
    "love",
    "great",
    "nope",
    "nice",
    "ok",
    "okay",
    "removed reddit",
    "right",
    "sad",
    "said",
    "s argument",
    "saying",
    "sure",
    "thank",
    "thanks",
    "tell levels",
    "think",
    "true",
    "youre okay clear history youre",
    "youre welcome",
    "wow",
    "wrong",
    "yeah",
    "yep",
    "yes",
    "got",
}
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _supports_noun_chunks(nlp) -> bool:
    return nlp.has_pipe("parser")


def load_nlp(model_name: str | None = None):
    selected_model = model_name or DEFAULT_CONFIG.spacy_model
    try:
        return spacy.load(selected_model)
    except OSError:
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        return nlp


def normalize_phrase(text: str, stopwords: set[str]) -> str | None:
    cleaned_text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = _TOKEN_RE.findall(cleaned_text)
    normalized_tokens = [token for token in tokens if token in REGIONAL_TERMS or token not in stopwords]
    if not normalized_tokens:
        return None
    phrase = " ".join(normalized_tokens).strip()
    if len(phrase) < 2:
        return None
    if phrase in EXCLUDED_PHRASES:
        return None
    if looks_like_argument_shell(normalized_tokens):
        return None
    if len(normalized_tokens) == 1 and normalized_tokens[0] not in KEEP_SINGLE_TOKEN_PHRASES:
        return None
    if is_generic_phrase(normalized_tokens):
        return None
    return phrase


def is_generic_phrase(tokens: list[str]) -> bool:
    if not tokens:
        return True
    if all(token in GENERIC_TOKENS for token in tokens):
        return True
    content_tokens = [token for token in tokens if token not in GENERIC_TOKENS]
    if not content_tokens:
        return True
    if len(tokens) <= 2 and len(content_tokens) == 1 and content_tokens[0] not in KEEP_SINGLE_TOKEN_PHRASES:
        return True
    return False


def looks_like_argument_shell(tokens: list[str]) -> bool:
    if not tokens:
        return True

    token_set = set(tokens)
    if "don" in token_set and "t" in token_set:
        return True
    if "s" in token_set and "argument" in token_set:
        return True
    if "glad" in token_set and "agree" in token_set:
        return True
    if "tell" in token_set and "levels" in token_set:
        return True
    if "okay" in token_set and "guy" in token_set:
        return True
    if "argument" in token_set and any(token in token_set for token in {"sale", "covered", "rules", "evidence"}):
        return True
    if "youre" in token_set and ("welcome" in token_set or "clear" in token_set):
        return True
    if "idea" in token_set and "talking" in token_set:
        return True
    if "common" in token_set and "sense" in token_set:
        return True
    if "aren" in token_set and "t" in token_set:
        return True
    return False


def extract_phrases_for_comment(text: str, nlp=None, model_name: str | None = None) -> list[str]:
    if not text.strip():
        return []

    nlp = nlp or load_nlp(model_name)
    normalized_text = normalize_text(text)
    doc = nlp(normalized_text)
    stopwords = nlp.Defaults.stop_words

    if _supports_noun_chunks(nlp):
        candidates = [chunk.text for chunk in doc.noun_chunks]
    else:
        candidates = [sent.text for sent in doc.sents]

    phrases: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        phrase = normalize_phrase(candidate, stopwords)
        if phrase and phrase not in seen:
            seen.add(phrase)
            phrases.append(phrase)
    return phrases


def extract_phrase_tables(comments: pl.DataFrame, nlp=None, model_name: str | None = None) -> tuple[pl.DataFrame, pl.DataFrame]:
    nlp = nlp or load_nlp(model_name)
    phrase_to_id: dict[str, str] = {}
    phrase_counts: dict[str, int] = defaultdict(int)
    phrase_first_seen: dict[str, datetime] = {}
    edges: list[dict[str, str]] = []

    for row in comments.iter_rows(named=True):
        comment_id = str(row["content_id"])
        created_at = row["created_at"]
        phrases = extract_phrases_for_comment(str(row.get("text", "")), nlp=nlp)
        for phrase in phrases:
            if phrase not in phrase_to_id:
                phrase_to_id[phrase] = f"phrase_{len(phrase_to_id) + 1:05d}"
            phrase_counts[phrase] += 1
            if phrase not in phrase_first_seen or created_at < phrase_first_seen[phrase]:
                phrase_first_seen[phrase] = created_at
            edges.append({"comment_id": comment_id, "phrase_id": phrase_to_id[phrase]})

    phrases_rows = [
        {
            "phrase_id": phrase_id,
            "phrase": phrase,
            "occurrence_count": phrase_counts[phrase],
            "first_seen": phrase_first_seen[phrase],
        }
        for phrase, phrase_id in sorted(phrase_to_id.items(), key=lambda item: item[1])
    ]

    phrases_schema = {
        "phrase_id": pl.Utf8,
        "phrase": pl.Utf8,
        "occurrence_count": pl.Int64,
        "first_seen": pl.Datetime(time_zone="UTC"),
    }
    edges_schema = {
        "comment_id": pl.Utf8,
        "phrase_id": pl.Utf8,
    }

    phrases_frame = pl.DataFrame(phrases_rows, schema=phrases_schema) if phrases_rows else pl.DataFrame(schema=phrases_schema)
    edges_frame = pl.DataFrame(edges, schema=edges_schema) if edges else pl.DataFrame(schema=edges_schema)
    return phrases_frame, edges_frame
