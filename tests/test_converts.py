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
