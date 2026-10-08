"""Smoke test: the package and core dependencies import correctly."""


def test_imports():
    import polars as pl
    import rapidfuzz
    import sklearn
    import splink

    import record_linkage

    assert record_linkage is not None
    assert all(m is not None for m in (pl, rapidfuzz, sklearn, splink))
