## Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.3] - 2025-11-10

### Fixed

- Fixed detection of optional Annotated date fields (`Annotated[date | None, format]`)
  - Now correctly identifies and formats fields with optional union annotations
  - Properly supports per-field format annotations with optional types

## [0.3.2] - 2025-11-07

### Added

- Support for `Annotated` date fields in DateSerializerMixin
  - Date fields wrapped in Pydantic's `Annotated` type hint are now properly detected and formatted
  - Enables use of annotated date fields with custom metadata

## [0.3.1] - 2025-11-05

### Changed

- Version bump for consistency with package versioning

## [0.3.0] - 2025-11-05

### Added

- **DateFormat class**: Lightweight wrapper for date format specifications
  - Provides type-safe format handling
  - Supports equality comparison and hashing
  - Works seamlessly with mixins
- **Predefined format constants** for convenience:
  - `ISO_FORMAT`: ISO 8601 format (YYYY-MM-DD)
  - `DMY_FORMAT`: European format (DD/MM/YYYY)
  - `MDY_FORMAT`: American format (MM/DD/YYYY)
  - `NUMBER_FORMAT`: Numeric format (YYYYMMDD)
- **Python 3.14 and Pydantic 2.12 support** with comprehensive edge case coverage
- **Per-field date format annotations** with Annotated support
- Enhanced README.md with comprehensive examples and use cases
  - Added section on using predefined format constants
  - Added section on creating custom date formats
- Updated CLAUDE.md with detailed development guidance
  - Documented DateFormat class architecture
  - Updated project overview with format constants
- Better error handling documentation with validation examples
- Comprehensive test suite for DateFormat and constants (16 new tests)

### Changed

- `__date_format__` ClassVar now accepts both string and DateFormat objects
- GitHub Actions workflow improvements for better CI/CD coverage
- Fixed gh-actions tox mapping to use specific Pydantic version combinations
- Fixed PyPI badge package name in README for correct version display

### Security

- Bandit security scanning enabled in CI/CD pipeline

## [0.2.0] - 2025-07-04

### Added

- Full type hints throughout codebase for better IDE support and type checking
- Comprehensive test coverage with mypy validation
- Linters integration in GitHub Actions workflow (flake8, pylint, bandit, mypy)

### Changed

- Improved code quality standards with stricter linting rules
- Enhanced type safety with full type annotations

### Removed

- Dropped Python 3.9 support (minimum now 3.10)
- Removed legacy type annotation patterns

## [0.1.2] - 2025-07-02

### Fixed

- Corrected version number in pyproject.toml
- Updated dependencies section structure for proper package metadata

## [0.1.1] - 2025-05-12

### Added

- **DateNumberSerializerMixin**: New mixin for YYYYMMDD integer format dates
  - Accepts integer dates in YYYYMMDD format
  - Serializes dates as integers instead of strings
  - Useful for legacy systems and numeric-based date storage

### Fixed

- Fixed Optional[date] field handling in DateSerializerMixin
  - Optional date fields now properly accept None values
  - Empty strings ("") correctly convert to None in string-based formats
  - Zero (0) correctly converts to None in numeric format
- Fixed typo in README.md documentation

## [0.1.0] - 2025-05-10

### Added

- Initial release with core date serialization functionality
- **DateSerializerMixin**: Generic mixin for customizable date formats (default: ISO YYYY-MM-DD)
- **DateDMYSerializerMixin**: Specialized mixin for European DD/MM/YYYY format
- Comprehensive test suite with 100% code coverage
- Full support for Pydantic v2.0+
- Support for Python 3.10, 3.11, 3.12, 3.13
- Automatic date field detection and validation
- JSON serialization/deserialization support

