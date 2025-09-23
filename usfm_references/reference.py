"""Reference class for parsing and representing USFM scripture references."""

from dataclasses import dataclass, field

from usfm_references.books import BOOK_CANON, BOOKS


@dataclass
class Reference:
    """
    Represents a USFM reference, including book, chapter, section, intro, and verse ranges.

    Verse ranges are sorted and intersecting or adjacent ranges are merged.

    Examples:
        ```python
        Reference.from_string("GEN.1")  # whole chapter
        Reference.from_string("GEN.1.1-3")  # verse range
        Reference.from_string("GEN.1.1+GEN.1.3")  # multiple verses
        Reference.from_string("GEN.INTRO1")  # intro chapter
        Reference.from_string("GEN.1_1.1")  # chapter with section
        Reference.from_string("GEN.1.1-3+GEN.1.5")  # multiple verses with range
        str(Reference.from_string("GEN.1"))  # "GEN.1"
        str(Reference.from_string("GEN.1.1+GEN.1.2+GEN.1.3"))  # "GEN.1.1-3"
        str(Reference.from_string("GEN.1.1+GEN.1.3"))  # "GEN.1.1+GEN.1.3"
        ```
    Raises:
        ValueError: if the reference string is invalid, such as having an incorrect format, unknown
        book code, or invalid chapter, section, intro, or verse numbers.
    """

    book: str = ""
    chapter: int = 0
    section: int = 0
    intro: int = 0
    verses: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        self._normalize_verses()

    @classmethod
    def from_string(cls, s: str) -> "Reference":
        """Parse a USFM reference string and return a Reference object."""
        s = s.strip()
        if not s:
            raise ValueError("empty reference")

        parts = s.split("+")
        ref = cls._parse_single(parts[0])
        is_full_chapter = ref.is_chapter()

        for part in parts[1:]:
            new_ref = cls._parse_single(part)
            if new_ref.is_chapter():
                is_full_chapter = True
            if ref.to_chapter_or_intro() != new_ref.to_chapter_or_intro():
                raise ValueError("references must be in the same chapter")
            ref.verses.extend(new_ref.verses)

        ref._normalize_verses()
        return ref.to_chapter_or_intro() if is_full_chapter else ref

    @classmethod
    def _parse_single(cls, s: str) -> "Reference":
        parts = s.split(".")
        if len(parts) not in (2, 3):
            raise ValueError(f"invalid USFM code {s}")

        book = parts[0]
        if len(book) != 3 or book not in BOOKS:
            raise ValueError(f"invalid USFM book code {book}")

        ref = cls(book=book)
        ref._parse_chapter(parts[1])
        if len(parts) == 3:
            ref._parse_verse_range(parts[2])
        return ref

    def _parse_chapter(self, chapter_str: str) -> None:
        if chapter_str.startswith("INTRO"):
            num = chapter_str.removeprefix("INTRO")
            if not num.isdigit() or int(num) < 1:
                raise ValueError(f"invalid intro reference {chapter_str}")
            self.intro = int(num)
            return

        # chapter[_section]
        parts = chapter_str.split("_", 1)
        if not parts[0].isdigit() or not 1 <= int(parts[0]) < 1000:
            raise ValueError(f"invalid chapter {chapter_str}")
        self.chapter = int(parts[0])

        if len(parts) == 2:
            if not parts[1].isdigit() or int(parts[1]) < 1:
                raise ValueError(f"invalid section {chapter_str}")
            self.section = int(parts[1])

    def _parse_verse_range(self, verse_str: str) -> None:
        parts = verse_str.split("-", 1)
        if not parts[0].isdigit():
            raise ValueError(f"invalid verse range {verse_str}")
        start = int(parts[0])
        if len(parts) == 2:
            if not parts[1].isdigit():
                raise ValueError(f"invalid verse range {verse_str}")
            end = int(parts[1])
        else:
            end = start
        if not 1 <= start <= end < 1000:
            raise ValueError(f"invalid verse range {verse_str}")
        self.verses.append((start, end))

    def _normalize_verses(self) -> None:
        if not self.verses:
            return
        self.verses.sort()
        merged = [self.verses[0]]
        for start, end in self.verses[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end + 1:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))
        self.verses = merged

    def __str__(self):
        """Return the USFM string representation of the reference."""
        if self.verses:
            ranges = [f"{s}" if s == e else f"{s}-{e}" for (s, e) in self.verses]
            return "+".join(f"{self.book}.{self._chapter_str()}.{r}" for r in ranges)
        if self.chapter:
            return f"{self.book}.{self._chapter_str()}"
        if self.intro:
            return f"{self.book}.INTRO{self.intro}"
        raise ValueError(
            "Internal error: Reference object is in an invalid state (missing chapter, intro, or verses)"  # pylint: disable=line-too-long
        )  # pragma: no cover

    def _chapter_str(self) -> str:
        return f"{self.chapter}" + ("_" + str(self.section) if self.section else "")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reference):  # pragma: no cover
            return False
        return (
            self.book == other.book
            and self.chapter == other.chapter
            and self.section == other.section
            and self.intro == other.intro
            and self.verses == other.verses
        )

    def is_chapter(self) -> bool:
        """Return True if the reference is a whole chapter."""
        return self.chapter > 0 and not self.verses

    def is_intro(self) -> bool:
        """Return True if the reference is an intro."""
        return self.intro > 0

    def is_single_verse(self) -> bool:
        """Return True if the reference is a single verse."""
        return self.chapter > 0 and len(self.verses) == 1 and self.verses[0][0] == self.verses[0][1]

    def is_verse_range(self) -> bool:
        """Return True if the reference is a verse range."""
        return self.chapter > 0 and len(self.verses) == 1 and self.verses[0][0] != self.verses[0][1]

    def to_chapter_or_intro(self) -> "Reference":
        """Return a Reference object representing only the chapter or intro (no verses)."""
        return Reference(
            book=self.book,
            chapter=self.chapter,
            section=self.section,
            intro=self.intro,
        )

    def to_single_verses(self) -> list["Reference"]:
        """Return a list of Reference objects, each for a single verse."""
        return [
            Reference(
                book=self.book,
                chapter=self.chapter,
                section=self.section,
                intro=self.intro,
                verses=[(v, v)],
            )
            for s, e in self.verses
            for v in range(s, e + 1)
        ]

    def to_verse_ranges(self) -> list["Reference"]:
        """Return a list of Reference objects, each for a single verse range."""
        return [
            Reference(
                book=self.book,
                chapter=self.chapter,
                section=self.section,
                intro=self.intro,
                verses=[r],
            )
            for r in self.verses
        ]

    @property
    def canon(self) -> str:
        """Return the canon category of the book (e.g., "ot", "nt", "ap")."""
        return BOOK_CANON.get(self.book, "ap")
