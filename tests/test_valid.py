"""
Test USFM validation
"""
import pytest

from usfm_references import (
    valid_chapter,
    valid_chapter_or_intro,
    valid_multi_usfm,
    valid_usfm,
    valid_verse,
    valid_passage,
)


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1", True),
        ("GEN.1_1", True),
        ("2TI.1_1", True),
        ("PSA.119", True),
        ("ZZZ.1", False),
        ("GEN.9999", False),
        ("Gen.1", False),  # Must be capitalized
        ("GEN.1-1", False),  # Underscored, not hyphenated
        ("GEN", False),  # Chapter required
    ],
)
def test_valid_chapter(ref, expect):
    """Test chapter reference validation."""
    assert valid_chapter(ref) == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1", True),
        ("GEN.1_1", True),
        ("2TI.1_1", True),
        ("2TI.INTRO1", True),
        ("GEN.INTRO5", True),
        ("PSA.119", True),
        ("ZZZ.1", False),
        ("GEN.9999", False),
        ("Gen.1", False),  # Must be capitalized
        ("GEN.1-1", False),  # Underscored, not hyphenated
        ("GEN", False),  # Chapter required
    ],
)
def test_valid_chapter_or_intro(ref, expect):
    """Test chapter or intro reference validation."""
    assert valid_chapter_or_intro(ref) == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1.1", True),
        ("GEN.000000.000000", False),
        ("1TI.300.9", True),
        ("PSA.119.1176", False),
        ("ZZZ.1.1", False),
        ("GEN.1_1", True),
        ("GEN.1_9999", True),
        ("REV.1_1.9999", False),
        ("Gen.1.1", False),  # must be capitalized
        ("Gen.1.1b", False),  # alpha not allowed in verse
        ("GEN.1.1_1", False),  # sub verses not allowed
        ("GEN", False),  # chapter required
    ],
)
def test_valid_usfm(ref, expect):
    """Test chapter reference validation."""
    assert valid_usfm(ref) == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1.1", True),
        ("1TI.1.1", True),
        ("PSA.999.999", True),
        ("REV.1_1.1", True),
        ("GEN.100000000.1", False),
        ("PSA.119.1176", False),
        ("ZZZ.1.1", False),
        ("GEN.1", False),  # verse required
        ("Gen.1.1", False),  # must be capitalized
        ("GEN.1.1_1", False),  # sub verses not allowed
        ("GEN", False),  # chapter & verse required
    ],
)
def test_valid_verse(ref, expect):
    """Test verse reference validation."""
    assert valid_verse(ref) == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1.1+GEN.1.2+GEN.1.3+GEN.1.4", True),
        ("GEN.1.1+GEN.1.2+GEN.1.3+GEN", False),
        ("GEN.000000.000000+GEN.1.1", False),
        ("1TI.300.9+1TI.1.1", True),
        ("PSA.119.1176", False),
        ("ZZZ.1.1+JA.1.1", False),
        ("GEN.1_1+GEN.1_2", True),
        ("GEN.1_9999+GEN.2_9999", True),
        ("REV.1_1.9999+REV.1_2.9999", False),
        ("Gen.1.1+Gen.1.2", False),  # must be capitalized
        ("Gen.1.1b+Gen1.1c", False),  # alpha not allowed in verse
        ("GEN.1.1_1+GEN.1.2_2", False),  # sub verses not allowed
        ("GEN+GEN", False),  # chapter required
    ],
)
def test_valid_multi_usfm_plus(ref, expect):
    """Test chapter reference validation."""
    assert valid_multi_usfm(ref) == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1.1,GEN.1.2,GEN.1.3,GEN.1.4", True),
        ("GEN.1.1,GEN.1.2,GEN.1.3,GEN", False),
        ("GEN.000000.000000,GEN.1.1", False),
        ("1TI.300.9,1TI.1.1", True),
        ("PSA.119.1176", False),
        ("ZZZ.1.1,JA.1.1", False),
        ("GEN.1_1,GEN.1_2", True),
        ("GEN.1_9999,GEN.2_9999", True),
        ("REV.1_1.9999,REV.1_2.9999", False),
        ("Gen.1.1,Gen.1.2", False),  # must be capitalized
        ("Gen.1.1b,Gen1.1c", False),  # alpha not allowed in verse
        ("GEN.1.1_1,GEN.1.2_2", False),  # sub verses not allowed
        ("GEN,GEN", False),  # chapter required
    ],
)
def test_valid_multi_usfm_comma(ref, expect):
    """Test chapter reference validation."""
    assert valid_multi_usfm(ref, delimiter=",") == expect


@pytest.mark.parametrize(
    "ref,expect",
    [
        ("GEN.1.1-GEN.1.4", False),
        ("GEN.1.1-GEN", False),
        ("GEN.000000.000000-1", False),
        ("PSA.119.1176-1177", False),
        ("ZZZ.1.1-2", False),
        ("GEN.1.1-2", True),
        ("REV.1_1.9999,REV.1_2.9999", False),
        ("Gen.1.1-2", False),  # must be capitalized
        ("Gen.1.1b-2c", False),  # alpha not allowed in verse
    ],
)
def test_valid_passage(ref, expect):
    """Test verse range validation."""
    assert valid_passage(ref) == expect
