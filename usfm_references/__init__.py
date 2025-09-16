"""
USFM References Tools
"""

import re
import typing

__version__ = "1.5.1"

ANY_REF = re.compile(r"^[1-9A-Z]{3}\.([0-9]{1,3}(_[0-9]+)?(\.[0-9]{1,3})?|INTRO\d+)$")
BOOKS = [
    "GEN",
    "EXO",
    "LEV",
    "NUM",
    "DEU",
    "JOS",
    "JDG",
    "RUT",
    "1SA",
    "2SA",
    "1KI",
    "2KI",
    "1CH",
    "2CH",
    "EZR",
    "NEH",
    "EST",
    "JOB",
    "PSA",
    "PRO",
    "ECC",
    "SNG",
    "ISA",
    "JER",
    "LAM",
    "EZK",
    "DAN",
    "HOS",
    "JOL",
    "AMO",
    "OBA",
    "JON",
    "MIC",
    "NAM",
    "HAB",
    "ZEP",
    "HAG",
    "ZEC",
    "MAL",
    "MAT",
    "MRK",
    "LUK",
    "JHN",
    "ACT",
    "ROM",
    "1CO",
    "2CO",
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "1TH",
    "2TH",
    "1TI",
    "2TI",
    "TIT",
    "PHM",
    "HEB",
    "JAS",
    "1PE",
    "2PE",
    "1JN",
    "2JN",
    "3JN",
    "JUD",
    "REV",
    "TOB",
    "JDT",
    "ESG",
    "WIS",
    "SIR",
    "BAR",
    "LJE",
    "S3Y",
    "SUS",
    "BEL",
    "1MA",
    "2MA",
    "3MA",
    "4MA",
    "1ES",
    "2ES",
    "MAN",
    "PS2",
    "ODA",
    "PSS",
    "EZA",
    "5EZ",
    "6EZ",
    "DAG",
    "PS3",
    "2BA",
    "LBA",
    "JUB",
    "ENO",
    "1MQ",
    "2MQ",
    "3MQ",
    "REP",
    "4BA",
    "LAO",
    "LKA",
    "3ES",
]

BOOK_CANON = {
    "GEN": "ot",
    "EXO": "ot",
    "LEV": "ot",
    "NUM": "ot",
    "DEU": "ot",
    "JOS": "ot",
    "JDG": "ot",
    "RUT": "ot",
    "1SA": "ot",
    "2SA": "ot",
    "1KI": "ot",
    "2KI": "ot",
    "1CH": "ot",
    "2CH": "ot",
    "EZR": "ot",
    "NEH": "ot",
    "EST": "ot",
    "JOB": "ot",
    "PSA": "ot",
    "PRO": "ot",
    "ECC": "ot",
    "SNG": "ot",
    "ISA": "ot",
    "JER": "ot",
    "LAM": "ot",
    "EZK": "ot",
    "DAN": "ot",
    "HOS": "ot",
    "JOL": "ot",
    "AMO": "ot",
    "OBA": "ot",
    "JON": "ot",
    "MIC": "ot",
    "NAM": "ot",
    "HAB": "ot",
    "ZEP": "ot",
    "HAG": "ot",
    "ZEC": "ot",
    "MAL": "ot",
    "MAT": "nt",
    "MRK": "nt",
    "LUK": "nt",
    "JHN": "nt",
    "ACT": "nt",
    "ROM": "nt",
    "1CO": "nt",
    "2CO": "nt",
    "GAL": "nt",
    "EPH": "nt",
    "PHP": "nt",
    "COL": "nt",
    "1TH": "nt",
    "2TH": "nt",
    "1TI": "nt",
    "2TI": "nt",
    "TIT": "nt",
    "PHM": "nt",
    "HEB": "nt",
    "JAS": "nt",
    "1PE": "nt",
    "2PE": "nt",
    "1JN": "nt",
    "2JN": "nt",
    "3JN": "nt",
    "JUD": "nt",
    "REV": "nt",
    "TOB": "ap",
    "JDT": "ap",
    "ESG": "ap",
    "WIS": "ap",
    "SIR": "ap",
    "BAR": "ap",
    "LJE": "ap",
    "S3Y": "ap",
    "SUS": "ap",
    "BEL": "ap",
    "1MA": "ap",
    "2MA": "ap",
    "3MA": "ap",
    "4MA": "ap",
    "1ES": "ap",
    "2ES": "ap",
    "MAN": "ap",
    "PS2": "ap",
    "ODA": "ap",
    "PSS": "ap",
    "3ES": "ap",
    "EZA": "ap",
    "5EZ": "ap",
    "6EZ": "ap",
    "DAG": "ap",
    "PS3": "ap",
    "2BA": "ap",
    "LBA": "ap",
    "JUB": "ap",
    "ENO": "ap",
    "1MQ": "ap",
    "2MQ": "ap",
    "3MQ": "ap",
    "REP": "ap",
    "4BA": "ap",
    "LAO": "ap",
    "LKA": "nt",  # luke-acts combo
}
CHAPTER = re.compile(r"^[1-6A-Z]{3}\.[0-9]{1,3}(_[0-9]+)?$")
CHAPTER_OR_INTRO = re.compile(r"^[1-9A-Z]{3}\.([0-9]{1,3}(_[0-9]+)?|INTRO\d+)$")
NT_BOOKS = [
    "MAT",
    "MRK",
    "LUK",
    "JHN",
    "ACT",
    "ROM",
    "1CO",
    "2CO",
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "1TH",
    "2TH",
    "1TI",
    "2TI",
    "TIT",
    "PHM",
    "HEB",
    "JAS",
    "1PE",
    "2PE",
    "1JN",
    "2JN",
    "3JN",
    "JUD",
    "REV",
]
OT_BOOKS = [
    "GEN",
    "EXO",
    "LEV",
    "NUM",
    "DEU",
    "JOS",
    "JDG",
    "RUT",
    "1SA",
    "2SA",
    "1KI",
    "2KI",
    "1CH",
    "2CH",
    "EZR",
    "NEH",
    "EST",
    "JOB",
    "PSA",
    "PRO",
    "ECC",
    "SNG",
    "ISA",
    "JER",
    "LAM",
    "EZK",
    "DAN",
    "HOS",
    "JOL",
    "AMO",
    "OBA",
    "JON",
    "MIC",
    "NAM",
    "HAB",
    "ZEP",
    "HAG",
    "ZEC",
    "MAL",
]
SINGLE_CHAPTER_OR_VERSE = re.compile(r"^([A-Za-z]{3})\.([1-9]+\.{0,1}[1-9]*)$")
VERSE = re.compile(r"^[1-6A-Z]{3}\.[0-9]{1,3}(_[0-9]+)?\.[0-9]{1,3}$")
VERSE_RANGE = re.compile(r"^[\d\s]*[-\w\s]+\d+:\d+-\d+$")


def convert_book_to_canon(book_usfm: str) -> str:
    """Get the canon str from a book usfm."""
    return BOOK_CANON.get(book_usfm, "ap")


# pylint: disable=inconsistent-return-statements
def convert_verse_range(ref: str) -> typing.Optional[list]:
    """Parse string to see if it is a range of verses."""
    if re.match(VERSE_RANGE, ref):
        book = re.findall(r"^([\d\s]*[-\w\s]+)\d+:\d+-\d+$", ref)[0]
        chapter = re.findall(r"^[\d\s]*[-\w\s]+(\d+):\d+-\d+$", ref)[0]
        first_verse = int(re.findall(r"^[\d\s]*[-\w\s]+\d+:(\d+)-\d+$", ref)[0])
        last_verse = int(re.findall(r"^[\d\s]*[-\w\s]+\d+:\d+-(\d+)$", ref)[0])

        hyphen_pos = ref.rfind("-")
        first_ref = ref[0:hyphen_pos]
        all_refs = [first_ref]
        for verse_number in range(first_verse + 1, last_verse + 1):
            all_refs.append(f"{book}{chapter}:{verse_number}")

        return all_refs


def valid_chapter(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible chapter reference.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length.
    """
    return bool(re.match(CHAPTER, ref) and ref.split(".")[0] in BOOKS)


def valid_chapter_or_intro(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible chapter reference or and INTRO.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length.
    OR
        followed by a period (.) and INTRO, followed by a number
    """
    return bool(CHAPTER_OR_INTRO.match(ref)) and ref.split(".")[0] in BOOKS


def valid_usfm(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible reference.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    """
    return bool(ANY_REF.match(ref)) and ref.split(".")[0] in BOOKS


def valid_verse(ref: str) -> bool:
    """
    Succeeds if the given string is a validly structured USFM Bible verse reference.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    """
    return bool(re.match(VERSE, ref) and ref.split(".")[0] in BOOKS)


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
    if any(not valid_usfm(usfm) for usfm in ref.split(delimiter)):
        return False
    return True


def valid_passage(passage: str) -> bool:
    """
    Succeeds if the given string is a validly structured Bible reference passage.
    A valid, capitalized (English) book abbreviation,
        followed by a period (.) and a (chapter) number of any length,
        optionally followed by an underscore (_) and a (sub-chapter?) number of any length,
        optionally followed by a period (.) and a (verse) number of any length.
    Multiple verses are seperated by with a hyphen and only the verse numbers.
    """
    try:
        book_id, chapter_id, verse_range = passage.split(".")
        if "-" in verse_range:
            start_verse, end_verse = verse_range.split("-")
            for i in range(int(start_verse), int(end_verse) + 1):
                if not valid_usfm(f"{book_id}.{chapter_id}.{i}"):
                    return False
        else:
            start_verse = verse_range  # only 1 verse
            if not valid_usfm(f"{book_id}.{chapter_id}.{start_verse}"):
                return False
    except Exception:
        return False
    return True
