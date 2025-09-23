"""
USFM References Tools
"""

from usfm_references.books import BOOK_CANON, BOOKS, NT_BOOKS, OT_BOOKS
from usfm_references.reference import Reference

__version__ = "2.0.0"


def convert_book_to_canon(book: str) -> str:
    """Return the canon category of a book (e.g., "ot", "nt", "ap")."""
    return BOOK_CANON.get(book, "ap")


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
        followed by a period (.) and a (chapter) number of any length,
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
