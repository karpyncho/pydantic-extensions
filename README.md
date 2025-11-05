# Karpyncho Pydantic Extensions

[![PyPI version](https://badge.fury.io/py/karpyncho-pydantic-extensions.svg)](https://badge.fury.io/py/karpyncho-pydantic-extensions)
[![Python versions](https://img.shields.io/pypi/pyversions/karpyncho-pydantic-extensions.svg)](https://pypi.org/project/karpyncho-pydantic-extensions/)
[![Tests](https://github.com/karpyncho/pydantic-extensions/actions/workflows/check.yml/badge.svg)](https://github.com/karpyncho/pydantic-extensions/actions/workflows/check.yml)
[![codecov](https://codecov.io/gh/karpyncho/pydantic-extensions/graph/badge.svg?token=swpOXcNXkz)](https://codecov.io/gh/karpyncho/pydantic-extensions)
[![Code Coverage](https://img.shields.io/badge/coverage-100%25-green)](https://codecov.io/gh/karpyncho/pydantic-extensions)
[![License: MIT](https://img.shields.io/github/license/karpyncho/pydantic-extensions)](https://github.com/karpyncho/pydantic-extensions/blob/main/LICENSE)
## Goal

A collection of extensions and enhancements for the Pydantic library, providing custom mixins and utilities to enhance your data validation and serialization capabilities.

## Features

- **Date Serialization**: Custom mixins for consistent date handling with configurable formats
  - `DateSerializerMixin`: Generic mixin for customizable date formats
  - `DateDMYSerializerMixin`: Specialized mixin for DD/MM/YYYY format
  - `DateNumberSerializerMixin`: Specialized mixin for YYYYMMDD format, serialized as an integer value instead of string

- **Predefined Format Constants**: Convenient format markers for common date formats
  - `ISO_FORMAT`: ISO 8601 format (YYYY-MM-DD)
  - `DMY_FORMAT`: European format (DD/MM/YYYY)
  - `MDY_FORMAT`: American format (MM/DD/YYYY)
  - `NUMBER_FORMAT`: Numeric format (YYYYMMDD)
  - `DateFormat`: Custom format class for defining your own formats

## Requirements

- **Python**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Pydantic**: >= 2.0 (tested with 2.0 through 2.12)

## Installation

```bash
pip install karpyncho-pydantic-extensions
```

Or with `pip` from the repository:

```bash
pip install git+https://github.com/karpyncho/pydantic-extensions.git
```

## Usage

### Basic Usage with DateSerializerMixin

The `DateSerializerMixin` provides a generic solution for handling date serialization with a customizable format:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateSerializerMixin

class Person(DateSerializerMixin, BaseModel):
    name: str
    birth_date: date
    
# The date will be formatted as YYYY-MM-DD (default format)
person = Person(name="John Doe", birth_date="2000-01-21")
print(person.model_dump())  # {'name': 'John Doe', 'birth_date': '2000-01-21'}

# You can also use date objects directly
person = Person(name="John Doe", birth_date=date(2000, 1, 21))
print(person.model_dump())  # {'name': 'John Doe', 'birth_date': '2000-01-21'}

# You can also deserialize a JSON string
json_str = '{"name": "John Doe", "birth_date": "2000-01-21"}'
person_dict = Person.loads(json_str)
person = Person(**person_dict)  
print(person)  # {'name': 'John Doe', 'birth_date': '2000-01-21'}

```

### Using DateDMYSerializerMixin for DD/MM/YYYY Format

For European date format (DD/MM/YYYY), use the specialized mixin:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateDMYSerializerMixin

class Person(DateDMYSerializerMixin, BaseModel):
    name: str
    birth_date: date

# The date will be formatted as DD/MM/YYYY
person = Person(name="John Doe", birth_date="21/01/2000")
print(person.model_dump())  # {'name': 'John Doe', 'birth_date': '21/01/2000'}

# You can also provide dates in different formats during initialization
person = Person(name="John Doe", birth_date=date(2000, 1, 21))
print(person.model_dump())  # {'name': 'John Doe', 'birth_date': '21/01/2000'}

# You can also deserialize a JSON string
json_str = '{"name": "John Doe", "birth_date": "21/01/2000"}'
import json
person_dict = json.loads(json_str)
person = Person(**person_dict)
print(person.model_dump())  # {'name': 'John Doe', 'birth_date': '21/01/2000'}
```

### Using DateNumberSerializerMixin for YYYYMMDD Integer Format

For numeric date format (YYYYMMDD as integers):

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateNumberSerializerMixin

class Transaction(DateNumberSerializerMixin, BaseModel):
    transaction_id: str
    transaction_date: date

# Accept integer dates in YYYYMMDD format
transaction = Transaction(transaction_id="TXN001", transaction_date=20231225)
print(transaction.model_dump())  # {'transaction_id': 'TXN001', 'transaction_date': 20231225}

# Also works with date objects
transaction = Transaction(transaction_id="TXN002", transaction_date=date(2023, 12, 25))
print(transaction.model_dump())  # {'transaction_id': 'TXN002', 'transaction_date': 20231225}
```

### Using Predefined Date Format Constants

The library provides convenient format constants for common date formats:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import (
    DateSerializerMixin,
    ISO_FORMAT,
    DMY_FORMAT,
    MDY_FORMAT,
    NUMBER_FORMAT,
)

# Using ISO format (default)
class Person(DateSerializerMixin, BaseModel):
    __date_format__ = ISO_FORMAT
    name: str
    birth_date: date

# Using European format
class PersonEU(DateSerializerMixin, BaseModel):
    __date_format__ = DMY_FORMAT
    name: str
    birth_date: date

# Using American format
class PersonUS(DateSerializerMixin, BaseModel):
    __date_format__ = MDY_FORMAT
    name: str
    birth_date: date

# Using numeric format
from karpyncho.pydantic_extensions import DateNumberSerializerMixin

class Transaction(DateNumberSerializerMixin, BaseModel):
    __date_format__ = NUMBER_FORMAT
    transaction_id: str
    transaction_date: date
```

Available predefined constants:
- `ISO_FORMAT`: ISO 8601 format `YYYY-MM-DD` (default)
- `DMY_FORMAT`: European format `DD/MM/YYYY`
- `MDY_FORMAT`: American format `MM/DD/YYYY`
- `NUMBER_FORMAT`: Numeric format `YYYYMMDD` (for integer serialization)

### Creating Custom Date Formats

You can create your own date format using the `DateFormat` class or by inheriting from `DateSerializerMixin`:

```python
from datetime import date
from typing import ClassVar
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateSerializerMixin, DateFormat

# Option 1: Using DateFormat class
custom_format = DateFormat("%d-%m-%Y")

class Person(DateSerializerMixin, BaseModel):
    __date_format__ = custom_format
    name: str
    birth_date: date

# Option 2: Creating a custom mixin
class DateCustomSerializerMixin(DateSerializerMixin):
    """Custom date format (DD-MM-YYYY)"""
    __date_format__: ClassVar[str] = "%d-%m-%Y"
```

### Per-Field Date Formats Using Annotations

You can override the date format on a per-field basis using the `Annotated` type hint. This allows different fields in the same model to use different date formats:

```python
from datetime import date
from typing import Annotated
from pydantic import BaseModel
from karpyncho.pydantic_extensions import (
    DateSerializerMixin,
    ISO_FORMAT,
    DMY_FORMAT,
    MDY_FORMAT,
    DateFormat,
)

class InternationalEvent(DateSerializerMixin, BaseModel):
    """Model with different date formats for different fields."""
    __date_format__ = ISO_FORMAT  # Default format

    event_name: str
    # European organizer - uses DD/MM/YYYY format
    eu_start_date: Annotated[date, DMY_FORMAT]
    # American organizer - uses MM/DD/YYYY format
    us_start_date: Annotated[date, MDY_FORMAT]
    # Default ISO format
    announcement_date: date

# Using the model
event = InternationalEvent(
    event_name="Global Conference",
    eu_start_date="15/06/2024",      # DD/MM/YYYY
    us_start_date="06/15/2024",      # MM/DD/YYYY
    announcement_date="2024-01-15"   # YYYY-MM-DD
)

print(event.model_dump())
# Output: {
#     'event_name': 'Global Conference',
#     'eu_start_date': '15/06/2024',
#     'us_start_date': '06/15/2024',
#     'announcement_date': '2024-01-15'
# }
```

You can also use custom `DateFormat` objects with annotations:

```python
from datetime import date
from typing import Annotated
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateSerializerMixin, DateFormat

class Report(DateSerializerMixin, BaseModel):
    title: str
    # Custom format: DD-MM-YYYY with dashes
    report_date: Annotated[date, DateFormat("%d-%m-%Y")]
    # Custom format: YYYY/MM/DD with slashes
    submission_date: Annotated[date, DateFormat("%Y/%m/%d")]

report = Report(
    title="Annual Report",
    report_date="25-12-2023",
    submission_date="2024/01/15"
)

print(report.model_dump())
# Output: {
#     'title': 'Annual Report',
#     'report_date': '25-12-2023',
#     'submission_date': '2024/01/15'
# }
```

**Key Benefits of Per-Field Annotations:**
- Override the default format on a per-field basis without creating multiple mixins
- Mix and match different date formats in the same model
- Maintain type safety with `Annotated` type hints
- Works seamlessly with all date field types (required and optional)

## Advanced Usage

### Multiple Date Fields

The mixins automatically handle all date fields in your model:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateDMYSerializerMixin

class Event(DateDMYSerializerMixin, BaseModel):
    title: str
    start_date: date
    end_date: date

event = Event(
    title="Conference",
    start_date="01/06/2023",
    end_date="05/06/2023"
)

print(event.model_dump())
# {'title': 'Conference', 'start_date': '01/06/2023', 'end_date': '05/06/2023'}
```

### Optional Date Fields

You can use optional date fields:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateDMYSerializerMixin

class Application(DateDMYSerializerMixin, BaseModel):
    applicant_name: str
    application_date: date
    approval_date: date | None = None

# Empty string or None becomes None for optional fields
app = Application(
    applicant_name="Jane Smith",
    application_date="15/03/2024",
    approval_date=""
)
print(app.approval_date)  # None

# Also works with DateNumberSerializerMixin
from karpyncho.pydantic_extensions import DateNumberSerializerMixin

class NumericApplication(DateNumberSerializerMixin, BaseModel):
    applicant_name: str
    application_date: date
    approval_date: date | None = None

# Zero becomes None for optional fields in numeric format
app = NumericApplication(
    applicant_name="John Doe",
    application_date=20240315,
    approval_date=0
)
print(app.approval_date)  # None
```

### Error Handling

The mixins include validation to ensure dates are provided in the correct format:

```python
from datetime import date
from pydantic import BaseModel
from pydantic import ValidationError
from karpyncho.pydantic_extensions import DateDMYSerializerMixin

class Person(DateDMYSerializerMixin, BaseModel):
    name: str
    birth_date: date

# This will raise a validation error for incorrect format
try:
    person = Person(name="John Doe", birth_date="2000-01-01")  # Wrong format
except ValidationError as e:
    print(f"Validation error: {e}")

# This will also raise an error for invalid dates
try:
    person = Person(name="Jane Doe", birth_date="32/13/2000")  # Invalid day/month
except ValidationError as e:
    print(f"Validation error: {e}")
```

### JSON Serialization

The mixins work seamlessly with Pydantic's JSON serialization:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateDMYSerializerMixin
import json

class Person(DateDMYSerializerMixin, BaseModel):
    name: str
    birth_date: date

person = Person(name="John Doe", birth_date="21/01/2000")

# Serialize to JSON
json_str = person.model_dump_json()
print(json_str)  # {"name":"John Doe","birth_date":"21/01/2000"}

# Deserialize from JSON
loaded = Person.model_validate_json(json_str)
print(loaded.birth_date)  # 2000-01-21
```

## How It Works

The mixins utilize Pydantic v2's initialization hooks and field validators to:

1. **Detect** all date fields automatically using `__pydantic_init_subclass__`
2. **Validate** and convert string/integer inputs to `date` objects using field validators
3. **Serialize** date objects to the specified format using `model_dump` override
4. **Encode** JSON dates using the `json_encoders` configuration

The `__date_format__` class variable controls the format string used by all methods.

## Use Cases

- **International Applications**: Handle dates in different formats based on locale (European DD/MM/YYYY vs American MM/DD/YYYY)
- **Legacy System Integration**: Work with legacy systems that use numeric date formats like YYYYMMDD
- **Financial/Banking Applications**: Consistent date formatting across transactions and reports
- **API Development**: Automatically serialize/deserialize dates in API requests and responses

## Supported Mixins Summary

| Mixin | Input Format | Output Format | Use Case |
|-------|--------------|---------------|----------|
| `DateSerializerMixin` | ISO (YYYY-MM-DD) | ISO (YYYY-MM-DD) | Standard/Default |
| `DateDMYSerializerMixin` | DD/MM/YYYY | DD/MM/YYYY | European format |
| `DateNumberSerializerMixin` | Integer YYYYMMDD | Integer YYYYMMDD | Numeric systems |
| Custom | User-defined | User-defined | Specific needs |

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/karpyncho/pydantic-extensions.git
cd pydantic-extensions

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest src

# Run with specific Pydantic version
tox -e py313-pydantic211

# Run with Python 3.14 and Pydantic 2.12
tox -e py314-pydantic212

# Run linters
tox -e linters
```

See [CLAUDE.md](./CLAUDE.md) for detailed development documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and ensure tests pass
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass (`pytest src`)
- Code coverage remains at 100% (required by CI)
- Linters pass (`tox -e linters`)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and changes.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
