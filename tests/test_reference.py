import pytest

from usfm_references.reference import Reference


@pytest.mark.parametrize(
    "string,reference",
    [
        (
            "GEN.1.1",
            Reference(book="GEN", chapter=1, verses=[(1, 1)]),
        ),
        (
            "GEN.1",
            Reference(book="GEN", chapter=1),
        ),
        (
            "GEN.INTRO1",
            Reference(book="GEN", intro=1),
        ),
        (
            "DAN.3.4-7",
            Reference(book="DAN", chapter=3, verses=[(4, 7)]),
        ),
        (
            "PSA.1_1.1+PSA.1_1.2+PSA.1_1.3",
            Reference(book="PSA", chapter=1, section=1, verses=[(1, 3)]),
        ),
        (
            "REV.1.2+REV.1.3+REV.1.4+REV.1.5+REV.1.6+REV.1.7",
            Reference(book="REV", chapter=1, verses=[(2, 7)]),
        ),
        (
            "GEN.1.1+GEN.1",
            Reference(book="GEN", chapter=1),
        ),
        (
            "GEN.1.2+GEN.1.1",
            Reference(book="GEN", chapter=1, verses=[(1, 2)]),
        ),
        (
            "GEN.1.3+GEN.1.1",
            Reference(book="GEN", chapter=1, verses=[(1, 1), (3, 3)]),
        ),
    ],
)
def test_reference_from_string(string, reference):
    """Test Reference.from_string."""
    assert Reference.from_string(string) == reference


@pytest.mark.parametrize(
    "string",
    [
        "",
        "GEN",
        "GEN.-1.1",
        "GEN.1+GEN.2",
        "GEN.1.2-1",
        "GEN.1.a",
        "GEN.1_A",
        "GEN.INTROA",
        "GENE.1.1",
    ],
)
def test_reference_from_string_failures(string):
    """Test Reference.from_string failure cases."""
    with pytest.raises(ValueError):
        Reference.from_string(string)


@pytest.mark.parametrize(
    "reference,string",
    [
        (
            Reference(book="GEN", intro=1),
            "GEN.INTRO1",
        ),
        (
            Reference(book="MAT", chapter=1),
            "MAT.1",
        ),
        (
            Reference(book="DAN", chapter=3, verses=[(4, 7)]),
            "DAN.3.4-7",
        ),
        (
            Reference(book="REV", chapter=1, verses=[(2, 7)]),
            "REV.1.2-7",
        ),
        (
            Reference(book="GEN", chapter=1, verses=[(1, 1), (3, 3)]),
            "GEN.1.1+GEN.1.3",
        ),
        (
            Reference(book="PSA", chapter=1, section=1, verses=[(1, 3)]),
            "PSA.1_1.1-3",
        ),
    ],
)
def test_reference_to_string(reference, string):
    """Test Reference.__str__."""
    assert str(reference) == string


def test_methods():
    """Test various Reference methods."""
    reference = Reference.from_string("GEN.1.1-3+GEN.1.5")
    assert reference.is_intro() is False
    assert reference.is_chapter() is False
    assert reference.is_single_verse() is False
    assert reference.is_verse_range() is False
    assert reference.to_verse_ranges() == [
        Reference(book="GEN", chapter=1, verses=[(1, 3)]),
        Reference(book="GEN", chapter=1, verses=[(5, 5)]),
    ]
    assert reference.to_single_verses() == [
        Reference(book="GEN", chapter=1, verses=[(1, 1)]),
        Reference(book="GEN", chapter=1, verses=[(2, 2)]),
        Reference(book="GEN", chapter=1, verses=[(3, 3)]),
        Reference(book="GEN", chapter=1, verses=[(5, 5)]),
    ]
    assert reference.canon == "ot"
