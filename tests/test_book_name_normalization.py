"""Prefix-normalization tests for convert_book_name_to_usfm (issue #31).

Numbered books no longer store every "1samuel/isamuel/firstsamuel" variant
as its own key; the leading ordinal is normalized (arabic / roman / word)
and the remaining stem is resolved. These tests pin that behavior across
every numbered book and guard the malformed cases.
"""

import pytest

import usfm_references


@pytest.mark.parametrize(
    "name,expect",
    [
        # --- Samuel: arabic / roman / word, full + abbreviations ---
        ("1 Samuel", "1SA"),
        ("2 Samuel", "2SA"),
        ("1Samuel", "1SA"),
        ("1 Sam", "1SA"),
        ("2 Sam", "2SA"),
        ("1 Sa", "1SA"),
        ("1 Sm", "1SA"),
        ("I Samuel", "1SA"),
        ("II Samuel", "2SA"),
        ("I Sam", "1SA"),
        ("II Sam", "2SA"),
        ("First Samuel", "1SA"),
        ("Second Samuel", "2SA"),
        # --- Kings ---
        ("1 Kings", "1KI"),
        ("2 Kings", "2KI"),
        ("1 Kgs", "1KI"),
        ("I Kings", "1KI"),
        ("II Kings", "2KI"),
        ("First Kings", "1KI"),
        ("Second Kings", "2KI"),
        # --- Chronicles ---
        ("1 Chronicles", "1CH"),
        ("2 Chronicles", "2CH"),
        ("1 Chron", "1CH"),
        ("1 Chr", "1CH"),
        ("II Chronicles", "2CH"),
        ("First Chronicles", "1CH"),
        # --- Corinthians ---
        ("1 Corinthians", "1CO"),
        ("2 Corinthians", "2CO"),
        ("1 Cor", "1CO"),
        ("I Corinthians", "1CO"),
        ("II Cor", "2CO"),
        ("Second Corinthians", "2CO"),
        # --- Thessalonians ---
        ("1 Thessalonians", "1TH"),
        ("2 Thessalonians", "2TH"),
        ("1 Thess", "1TH"),
        ("2 Thes", "2TH"),
        ("II Thessalonians", "2TH"),
        ("First Thessalonians", "1TH"),
        # --- Timothy ---
        ("1 Timothy", "1TI"),
        ("2 Timothy", "2TI"),
        ("1 Tim", "1TI"),
        ("II Timothy", "2TI"),
        ("Second Timothy", "2TI"),
        # --- Peter ---
        ("1 Peter", "1PE"),
        ("2 Peter", "2PE"),
        ("1 Pet", "1PE"),
        ("I Peter", "1PE"),
        ("Second Peter", "2PE"),
        # --- John (1-3; the bare gospel stays JHN) ---
        ("John", "JHN"),
        ("1 John", "1JN"),
        ("2 John", "2JN"),
        ("3 John", "3JN"),
        ("1 Jn", "1JN"),
        ("III John", "3JN"),
        ("II John", "2JN"),
        ("First John", "1JN"),
        ("Third John", "3JN"),
        # --- Maccabees ---
        ("1 Maccabees", "1MA"),
        ("2 Maccabees", "2MA"),
        ("1 Macc", "1MA"),
        ("II Maccabees", "2MA"),
        ("First Maccabees", "1MA"),
        # --- Esdras ---
        ("1 Esdras", "1ES"),
        ("2 Esdras", "2ES"),
        ("1 Esd", "1ES"),
        ("II Esdras", "2ES"),
        # --- mixed case / punctuation / whitespace still normalize ---
        ("first samuel", "1SA"),
        ("ii  samuel", "2SA"),
        ("1 Cor.", "1CO"),
        ("  III John  ", "3JN"),
    ],
)
def test_numbered_prefix_normalization(name, expect):
    assert usfm_references.convert_book_name_to_usfm(name) == expect


@pytest.mark.parametrize(
    "name",
    [
        # ordinal out of range for the book
        "4 John",
        "5 John",
        "3 Samuel",
        "3 Kings",
        "3 Corinthians",
        "4 Maccabees",
        "0 Samuel",
        # malformed roman numerals
        "IIV Samuel",
        "IV Samuel",
        "VI John",
        # a bare numbered stem with no ordinal is not a book
        "Samuel",
        "Kings",
        "Corinthians",
        # misspelled book names
        "Samuell",
        "Corintians",
        # misspelled / non-ordinal prefixes
        "Frist John",
        "Twoth Samuel",
    ],
)
def test_invalid_numbered_inputs_return_none(name):
    assert usfm_references.convert_book_name_to_usfm(name) is None
