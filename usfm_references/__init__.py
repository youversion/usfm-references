"""
USFM References Tools
"""

import re
from typing import Optional

from usfm_references.books import (
    BOOK_CANON,
    BOOK_NAMES,
    BOOKS,
    NT_BOOKS,
    NUMBERED_BOOKS,
    ORDINAL_WORDS,
    OT_BOOKS,
    ROMAN_ORDINALS,
)
from usfm_references.reference import Reference

__version__ = "3.1.1"

_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]")
_LEADING_DIGITS = re.compile(r"^(\d+)(.+)$")


def _split_leading_ordinal(key):
    """
    Split a leading ordinal off a normalized book key.

    Recognizes arabic digits ("1john"), the roman forms I/II/III
    ("iijohn"), and the words First/Second/Third ("firstjohn"). Returns
    ``(number, remainder)`` for the first form that leaves a non-empty
    remainder, or ``None`` when the key has no leading ordinal.
    """
    digits = _LEADING_DIGITS.match(key)
    if digits:
        return int(digits.group(1)), digits.group(2)
    for word, value in ORDINAL_WORDS.items():
        if key.startswith(word) and len(key) > len(word):
            return value, key[len(word) :]
    # Longest first so "iii"/"ii" win over the "i" prefix.
    for roman, value in sorted(ROMAN_ORDINALS.items(), key=lambda kv: -len(kv[0])):
        if key.startswith(roman) and len(key) > len(roman):
            return value, key[len(roman) :]
    return None


def convert_book_to_canon(book: str) -> str:
    """Return the canon category of a book (e.g., "ot", "nt", "ap")."""
    return BOOK_CANON.get(book, "ap")


def convert_book_name_to_usfm(name: str) -> Optional[str]:
    """
    Return the USFM book code for an English book name or common abbreviation.

    The input is matched case-insensitively and ignores whitespace and
    punctuation, so "Genesis", "genesis", "Gen", "Gen.", and "  GENESIS  "
    all return "GEN". Numbered books accept arabic, roman, and word forms:
    "1 Samuel", "1Sam", "I Sam", and "First Samuel" all return "1SA". A USFM
    code passed in directly (e.g., "GEN") is returned as-is. Returns None
    when no match is found.
    """
    if not name:
        return None
    stripped = name.strip()
    if stripped in BOOKS:
        return stripped
    key = _NON_ALPHANUMERIC.sub("", stripped.lower())
    if not key:
        return None
    if key in BOOK_NAMES:
        return BOOK_NAMES[key]
    # Numbered books store each stem once; peel the leading ordinal
    # (arabic/roman/word) and resolve the remainder. Unknown stems or
    # out-of-range ordinals (e.g. "4 John") fall through to None.
    split = _split_leading_ordinal(key)
    if split:
        number, stem = split
        return NUMBERED_BOOKS.get(stem, {}).get(number)
    return None


def valid_chapter(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible chapter reference.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length.
    """
    try:
        return Reference.from_string(ref).is_chapter()
    except ValueError:
        return False


def valid_chapter_or_intro(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible chapter reference or and INTRO.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length.
    OR
        followed by a period (.) and INTRO, followed by a number
    """
    try:
        reference = Reference.from_string(ref)
        return reference.is_chapter() or reference.is_intro()
    except ValueError:
        return False


def valid_usfm(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible reference.
    A valid, capitalized (English) book abbreviation,
        optionally followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    """
    try:
        Reference.from_string(ref)
        return True
    except ValueError:
        return False


def valid_verse(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible single verse reference.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    """
    try:
        return Reference.from_string(ref).is_single_verse()
    except ValueError:
        return False


def valid_multi_usfm(ref: str, delimiter: str = "+") -> bool:
    """
    Succeeds if the given string is a validly structured set of UFM Bible references.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    Multiple verses are seperated by a plus (+)
    Example Multi USFM ref (James1:1-5): JAS.1.1+JAS.1.2+JAS.1.3+JAS.1.4+JAS.1.5
    Another Example with COMMA delimiter: JAS.1.1,JAS.1.2,JAS.1.3,JAS.1.4,JAS.1.5
    """
    try:
        reference = Reference.from_string(ref.replace(delimiter, "+"))
        return len(reference.to_single_verses()) > 1
    except ValueError:
        return False


def valid_passage(passage: str) -> bool:
    """
    Succeeds if the given string is a validly structured Bible reference passage.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    Multiple verses are separated by a hyphen and only the verse numbers.
    """
    return valid_usfm(passage)
