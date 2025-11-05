# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Karpyncho Pydantic Extensions** is a Python package that provides custom mixins and utilities for the Pydantic library, with a focus on date serialization. The library offers:

### Mixins
- `DateSerializerMixin`: Generic mixin for customizable date formats (default: ISO format YYYY-MM-DD)
- `DateDMYSerializerMixin`: Specialized mixin for DD/MM/YYYY format
- `DateNumberSerializerMixin`: Specialized mixin for YYYYMMDD format, serialized as integers

### Format Constants
- `ISO_FORMAT`: ISO 8601 format (YYYY-MM-DD)
- `DMY_FORMAT`: European format (DD/MM/YYYY)
- `MDY_FORMAT`: American format (MM/DD/YYYY)
- `NUMBER_FORMAT`: Numeric format (YYYYMMDD)
- `DateFormat`: Custom format class for user-defined formats

## Key Architecture

### Mixin Design Pattern
The library uses a class-based mixin approach that leverages Pydantic v2's hooks and validators:

1. **Field Detection**: The `__pydantic_init_subclass__` hook identifies all `date` fields in the model during class initialization
2. **Validation**: A field validator (`validate_date_format`) handles deserialization - converting string/int inputs to `date` objects
3. **Serialization**: The `model_dump` method is overridden to format dates according to the specified format

### Protocol-Based Design
The `PydanticModelProtocol` is used to define the expected Pydantic interface, ensuring type safety when the mixin interacts with BaseModel classes.

### Class Variables
- `__date_fields__`: Set of field names that are date types (collected per subclass)
- `__date_format__`: ClassVar defining the format (can be string or DateFormat object, overrideable in subclasses)
- `model_config`: ConfigDict that includes json_encoders for date formatting

### DateFormat Class
The `DateFormat` class is a lightweight wrapper around strftime format strings that provides:
- String representation (`__str__`)
- Proper repr for debugging
- Equality comparison based on format string
- Hashability for use in sets/dicts
- Type safety when passing format specifications

Mixins automatically handle both string and DateFormat objects by calling `str()` on `__date_format__`

## Code Structure

```
src/
├── karpyncho/
│   └── pydantic_extensions/
│       └── __init__.py          # All mixins and protocol defined here
└── tests/
    └── test_pydantic_extensions.py  # Comprehensive test suite
```

## Common Commands

### Run Tests
```bash
pytest src                                    # Run all tests
pytest src::test_module::TestClass::test_name # Run specific test
pytest src -v                                 # Verbose output
```

### Run Single Test File
```bash
pytest src/tests/test_pydantic_extensions.py -v
```

### Linting and Code Quality
```bash
tox -e flake8      # Run flake8 linter
tox -e pylint      # Run pylint linter
tox -e bandit      # Run bandit security check
tox -e mypy        # Run mypy type checker
tox -e linters     # Run all linters together
```

### Run Tests with Multiple Pydantic Versions
```bash
tox -e py313-pydantic211    # Test against specific Python/Pydantic version
tox -e py314-pydantic212    # Test against Python 3.14 with Pydantic 2.12
tox                         # Run full test matrix (all Python 3.10-3.14, Pydantic 2.0-2.12)
```

### Coverage
```bash
tox -e py313-cov           # Run tests with coverage report (must be 100%)
pytest src --cov=. --cov-report=html  # HTML coverage report
```

### Build Package
```bash
python -m build            # Build distribution files
```

## Important Development Notes

### Pydantic Version Support
- Minimum required: Pydantic >= 2.0
- Tested against: Pydantic 2.0 through 2.12 (via tox matrix)
- Python versions: 3.10, 3.11, 3.12, 3.13, 3.14

### Test Coverage
- **Requirement**: 100% code coverage is enforced (see tox.ini `py313-cov` environment)
- Tests are comprehensive and cover both serialization and deserialization for all mixins
- Handle edge cases like empty strings, None values, and invalid formats

### Field Detection Mechanism
When working with the mixins, understand that `__pydantic_init_subclass__` is called when a subclass is created. The `__date_fields__` set is populated by inspecting `model_fields` and checking for `date` or `date | None` annotations. This means:
- Only explicitly typed `date` fields are handled
- Optional dates (`date | None`) are supported
- The detection happens once per class definition, not per instance

### Validator Behavior
- The `validate_date_format` validator uses Pydantic's `mode="before"` to intercept input before normal validation
- For `DateNumberSerializerMixin`, the validator specifically handles integer inputs
- Empty strings (`""`) are converted to `None` for optional fields
- Zero (`0`) is treated as `None` for `DateNumberSerializerMixin`'s optional fields

### JSON Encoding
The `json_encoders` in `model_config` ensures that when Pydantic's `model_dump_json()` is called, dates are formatted correctly. However, the mixins also override `model_dump()` for consistency.

## Linting Configuration

- **Max line length**: 120 characters (configured in tox.ini)
- **Flake8 plugins**: flake8-import-order, pep8-naming, flake8-colors
- **Type checking**: mypy with incomplete features enabled (`--enable-incomplete-feature=Unpack`)

## GitHub Actions Workflow

The `.github/workflows/check.yml` runs:
1. Test matrix against Python 3.10-3.13 on Ubuntu
2. Coverage check (must be 100%) with Pydantic 2.11
3. Linters check (flake8, pylint, bandit, mypy)

## Publishing

The package is published to PyPI via `.github/workflows/python-publish.yml` when tags are pushed.
