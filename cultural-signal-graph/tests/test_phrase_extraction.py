from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

from csg.cli.extract_phrases import run_phrase_extraction
from csg.extract.phrases import extract_phrase_tables, is_generic_phrase, looks_like_argument_shell, normalize_phrase


class FakeChunk:
    def __init__(self, text: str) -> None:
        self.text = text


class FakeSentence:
    def __init__(self, text: str) -> None:
        self.text = text


class FakeDoc:
    def __init__(self, noun_chunks: list[str], text: str) -> None:
        self.noun_chunks = [FakeChunk(chunk) for chunk in noun_chunks]
        self.sents = [FakeSentence(text)]


class FakeNLP:
    pipe_names = ["parser"]

    class Defaults:
        stop_words = {"the", "a", "an", "in", "of", "to", "and"}

    def __call__(self, text: str) -> FakeDoc:
        mapping = {
            "traffic near hrbt and vb is brutal": ["traffic near HRBT", "VB"],
            "ghent food scene in norfolk is growing": ["Ghent food scene", "Norfolk"],
        }
        return FakeDoc(mapping.get(text, []), text)

    def has_pipe(self, name: str) -> bool:
        return name == "parser"


def test_normalize_phrase_preserves_regional_terms() -> None:
    stopwords = FakeNLP.Defaults.stop_words
    assert normalize_phrase("Traffic near HRBT", stopwords) == "traffic near hrbt"
    assert normalize_phrase("VB", stopwords) == "vb"
    assert normalize_phrase("Norfolk", stopwords) == "norfolk"
    assert normalize_phrase("Texas", stopwords) == "texas"


def test_normalize_phrase_excludes_conversational_fillers() -> None:
    stopwords = FakeNLP.Defaults.stop_words
    assert normalize_phrase("yes", stopwords) is None
    assert normalize_phrase("lol", stopwords) is None
    assert normalize_phrase("right", stopwords) is None
    assert normalize_phrase("thank", stopwords) is None
    assert normalize_phrase("ok", stopwords) is None
    assert normalize_phrase("wow", stopwords) is None
    assert normalize_phrase("removed reddit", stopwords) is None
    assert normalize_phrase("wrong", stopwords) is None
    assert normalize_phrase("fuck", stopwords) is None
    assert normalize_phrase("lmao", stopwords) is None
    assert normalize_phrase("like", stopwords) is None
    assert normalize_phrase("correct", stopwords) is None
    assert normalize_phrase("love", stopwords) is None
    assert normalize_phrase("sad", stopwords) is None
    assert normalize_phrase("got", stopwords) is None
    assert normalize_phrase("nice", stopwords) is None
    assert normalize_phrase("great", stopwords) is None
    assert normalize_phrase("saying", stopwords) is None
    assert normalize_phrase("think", stopwords) is None
    assert normalize_phrase("cool", stopwords) is None
    assert normalize_phrase("oh", stopwords) is None
    assert normalize_phrase("believe", stopwords) is None
    assert normalize_phrase("point", stopwords) is None
    assert normalize_phrase("try", stopwords) is None
    assert normalize_phrase("im", stopwords) is None
    assert normalize_phrase("course", stopwords) is None
    assert normalize_phrase("aren t", stopwords) is None
    assert normalize_phrase("youre welcome", stopwords) is None
    assert normalize_phrase("common sense", stopwords) is None


def test_generic_phrase_filter_rejects_low_information_chunks() -> None:
    assert is_generic_phrase(["cool"]) is True
    assert is_generic_phrase(["good", "day"]) is True
    assert is_generic_phrase(["nice", "deflection"]) is True
    assert is_generic_phrase(["patriot", "front"]) is False
    assert is_generic_phrase(["texas"]) is False


def test_argument_shell_filter_rejects_reply_fragments() -> None:
    assert looks_like_argument_shell(["don", "t"]) is True
    assert looks_like_argument_shell(["s", "argument"]) is True
    assert looks_like_argument_shell(["glad", "agree"]) is True
    assert looks_like_argument_shell(["tell", "levels"]) is True
    assert looks_like_argument_shell(["okay", "guy"]) is True
    assert looks_like_argument_shell(["argument", "sale", "books", "covered", "1a"]) is True
    assert looks_like_argument_shell(["youre", "welcome"]) is True
    assert looks_like_argument_shell(["youre", "okay", "clear", "history", "youre"]) is True
    assert looks_like_argument_shell(["idea", "talking"]) is True
    assert looks_like_argument_shell(["common", "sense"]) is True
    assert looks_like_argument_shell(["aren", "t"]) is True
    assert looks_like_argument_shell(["patriot", "front"]) is False


def test_extract_phrase_tables_with_example_comments() -> None:
    comments = pl.DataFrame(
        [
            {
                "content_id": "c1",
                "text": "Traffic near HRBT and VB is brutal",
                "created_at": datetime(2026, 3, 13, 12, 0, tzinfo=timezone.utc),
            },
            {
                "content_id": "c2",
                "text": "Ghent food scene in Norfolk is growing",
                "created_at": datetime(2026, 3, 13, 13, 0, tzinfo=timezone.utc),
            },
        ]
    )

    phrases, edges = extract_phrase_tables(comments, nlp=FakeNLP())
    assert set(phrases["phrase"].to_list()) == {"traffic near hrbt", "vb", "ghent food scene", "norfolk"}
    assert edges.height == 4
    assert set(edges["comment_id"].to_list()) == {"c1", "c2"}


def test_run_phrase_extraction_writes_parquet(tmp_path) -> None:
    input_path = tmp_path / "comments.parquet"
    phrases_output = tmp_path / "phrases.parquet"
    edges_output = tmp_path / "comment_phrase_edges.parquet"

    pl.DataFrame(
        [
            {
                "content_id": "c1",
                "text": "Traffic near HRBT and VB is brutal",
                "created_at": datetime(2026, 3, 13, 12, 0, tzinfo=timezone.utc),
            }
        ]
    ).write_parquet(input_path)

    run_phrase_extraction(input_path, phrases_output, edges_output)

    assert phrases_output.exists()
    assert edges_output.exists()
