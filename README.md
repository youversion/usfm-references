# usfm-references

[![Build Status](https://travis-ci.org/bbelyeu/usfm-references.svg?branch=main)](https://travis-ci.org/bbelyeu/usfm-references)
[![Coverage Status](https://coveralls.io/repos/github/bbelyeu/usfm-references/badge.svg?branch=main)](https://coveralls.io/github/bbelyeu/usfm-references?branch=main)
[![Python versions](https://img.shields.io/pypi/pyversions/usfm-references?color=blue)](https://pypi.org/project/usfm-references)

Utilities for parsing, validating and manipulating USFM (Unified Standard Format Markers)
references.

This library provides:

- validators for USFM strings (verse, chapter, intro, multi references)
- a Reference model for composing and formatting references

## Requirements

Python 3.9 or newer. The project CI runs on 3.9–3.12.

## Installation

Install from PyPI:

```bash
pip install usfm-references
```

## Quick Usage

Validate USFM reference strings using the `valid_` helpers:

```python
from usfm_references import valid_verse, valid_chapter, valid_multi_usfm

valid_verse("GEN.1.1")               # True
valid_chapter("GEN.1")               # True
valid_multi_usfm("GEN.1.1+GEN.1.3")  # True
```

Get a book's canon grouping:

```python
from usfm_references import convert_book_to_canon

convert_book_to_canon("GEN")  # 'ot'
```

## Reference Model

The `Reference` dataclass is a convenient way to parse, build and format USFM references. It
normalizes verse ranges (they are kept sorted and merged when intersecting or adjacent).

Examples:

```python
from usfm_references import Reference

Reference.from_string("GEN.1")                # whole chapter -> Reference(book='GEN', chapter=1)
Reference.from_string("GEN.1.1-3")            # verse range -> verses [(1, 3)]
Reference.from_string("GEN.1.1+GEN.1.3")      # multiple verses -> verses [(1, 1), (3, 3)]
Reference.from_string("GEN.INTRO1")           # intro chapter -> intro=1

# Overlapping/adjacent ranges are merged:
str(Reference.from_string("GEN.1.1+GEN.1.2+GEN.1.3"))  # 'GEN.1.1-3'
```

## Development

For local development, create a venv and install dev dependencies (project uses pip-tools):

```bash
make venv
```

Run linting and formatting:

```bash
make lint
```

Run tests:

```bash
make test
```

A pre-commit hook is provided to lint and run tests before each commit. To install it, run:

```bash
(cd .git/hooks && ln -s ../../pre-commit pre-commit)
```
