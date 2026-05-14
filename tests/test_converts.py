"""Test convert methods."""

import pytest

import usfm_references


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN", "ot"),
        ("NEH", "ot"),
        ("MAT", "nt"),
        ("REV", "nt"),
        ("LKA", "nt"),
        ("PS2", "ap"),
    ],
)
def test_convert_book_to_canon(ref, expect):
    """Test chapter reference validation."""
    assert usfm_references.convert_book_to_canon(ref) == expect


@pytest.mark.parametrize(
    "name,expect",
    [
        # Full names
        ("Genesis", "GEN"),
        ("Exodus", "EXO"),
        ("Deuteronomy", "DEU"),
        ("Song of Songs", "SNG"),
        ("Song of Solomon", "SNG"),
        ("Ecclesiastes", "ECC"),
        ("Lamentations", "LAM"),
        ("Matthew", "MAT"),
        ("John", "JHN"),
        ("Revelation", "REV"),
        ("Apocalypse", "REV"),
        # Common short forms
        ("Gen", "GEN"),
        ("Gn", "GEN"),
        ("Exod", "EXO"),
        ("Ex", "EXO"),
        ("Deut", "DEU"),
        ("Dt", "DEU"),
        ("Josh", "JOS"),
        ("Judg", "JDG"),
        ("Ps", "PSA"),
        ("Pss", "PSA"),
        ("Eccl", "ECC"),
        ("Qoheleth", "ECC"),
        ("Cant", "SNG"),
        ("Ezek", "EZK"),
        ("Obad", "OBA"),
        ("Matt", "MAT"),
        ("Mt", "MAT"),
        ("Mk", "MRK"),
        ("Lk", "LUK"),
        ("Jn", "JHN"),
        ("Rev", "REV"),
        ("Phlm", "PHM"),
        # Numbered books — arabic, no space
        ("1Samuel", "1SA"),
        ("1Sam", "1SA"),
        ("1Sa", "1SA"),
        ("2Kings", "2KI"),
        ("1Cor", "1CO"),
        ("2Cor", "2CO"),
        ("3John", "3JN"),
        # Numbered books — arabic, with space
        ("1 Samuel", "1SA"),
        ("2 Samuel", "2SA"),
        ("1 Kings", "1KI"),
        ("1 Chronicles", "1CH"),
        ("1 Corinthians", "1CO"),
        ("1 Thessalonians", "1TH"),
        ("1 Timothy", "1TI"),
        ("1 Peter", "1PE"),
        ("1 John", "1JN"),
        # Numbered books — roman numeral form
        ("I Samuel", "1SA"),
        ("II Samuel", "2SA"),
        ("I Kings", "1KI"),
        ("III John", "3JN"),
        # Numbered books — word form
        ("First Samuel", "1SA"),
        ("Second Kings", "2KI"),
        ("Third John", "3JN"),
        # Case insensitivity
        ("genesis", "GEN"),
        ("GENESIS", "GEN"),
        ("gEnEsIs", "GEN"),
        # Surrounding whitespace
        ("  Genesis  ", "GEN"),
        ("\tMatthew\n", "MAT"),
        # Trailing punctuation
        ("Gen.", "GEN"),
        ("Matt.", "MAT"),
        ("1 Cor.", "1CO"),
        # Internal whitespace and punctuation collapse
        ("1  Samuel", "1SA"),
        ("Song  of  Songs", "SNG"),
        # USFM codes pass through unchanged
        ("GEN", "GEN"),
        ("1SA", "1SA"),
        ("REV", "REV"),
        ("PHP", "PHP"),
        # Apocrypha
        ("Tobit", "TOB"),
        ("Judith", "JDT"),
        ("Wisdom", "WIS"),
        ("Wisdom of Solomon", "WIS"),
        ("Sirach", "SIR"),
        ("Ecclesiasticus", "SIR"),
        ("Baruch", "BAR"),
        ("Susanna", "SUS"),
        ("Bel and the Dragon", "BEL"),
        ("1 Maccabees", "1MA"),
        ("2 Maccabees", "2MA"),
        ("1 Esdras", "1ES"),
        ("Prayer of Manasseh", "MAN"),
    ],
)
def test_convert_book_name_to_usfm(name, expect):
    """Test book name to USFM lookup."""
    assert usfm_references.convert_book_name_to_usfm(name) == expect


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
        "Nope",
        "Book of Mormon",
        "Quran",
        "12345",
        "ZZZ",
        "4 Maccabees Plus",
    ],
)
def test_convert_book_name_to_usfm_returns_none(name):
    """Test that unrecognized names return None."""
    assert usfm_references.convert_book_name_to_usfm(name) is None
