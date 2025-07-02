# Karpyncho Pydantic Extensions

[![PyPI version](https://badge.fury.io/py/karpyncho-pydantic-extensions.svg)](https://badge.fury.io/py/karpyncho-pydantic-extensions)
[![PyPI version](https://img.shields.io/pypi/v/pydantic-extensions.svg)](https://pypi.org/project/karpyncho-pydantic-extensions/)

[![Python versions](https://img.shields.io/pypi/pyversions/pydantic-extensions.svg)](https://pypi.org/project/karpyncho-pydantic-extensions/)

[![check](https://github.com/karpyncho/pydantic-extensions/actions/workflows/check.yml/badge.svg)](https://github.com/karpyncho/pydantic-extensions/actions/workflows/check.yml)
[![codecov](https://codecov.io/gh/karpyncho/pydantic-extensions/graph/badge.svg?token=swpOXcNXkz)](https://codecov.io/gh/karpyncho/pydantic-extensions)
[![GitHub License](https://img.shields.io/github/license/karpyncho/pydantic-extensions)](https://github.com/karpyncho/pydantic-extensions/blob/main/LICENSE)
## Goal

A collection of extensions and enhancements for the Pydantic library, providing custom mixins and utilities to enhance your data validation and serialization capabilities.

## Features

- **Date Serialization**: Custom mixins for consistent date handling with configurable formats
  - `DateSerializerMixin`: Generic mixin for customizable date formats
  - `DateDMYSerializerMixin`: Specialized mixin for DD/MM/YYYY format
  - `DateNumberSerializerMixin`: Specialized mixin for YYYYMMDD format, serialized as an integer value instead of string

## Installation

```bash
pip install pydantic-extensions
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
person_dict = Person.loads(json_str)
person = Person(**person_dict)  
print(person)  # {'name': 'John Doe', 'birth_date': '21/01/2000'}
```

### Creating Custom Date Format Mixins

You can create your own date format mixins by inheriting from `DateSerializerMixin`:

```python
from karpyncho.pydantic_extensions import DateSerializerMixin
from typing import ClassVar

class DateMDYSerializerMixin(DateSerializerMixin):
    """American-style date format (MM/DD/YYYY)"""
    __date_format__: ClassVar[str] = "%m/%d/%Y"
```

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

### Error Handling

The mixins include validation to ensure dates are provided in the correct format:

```python
from datetime import date
from pydantic import BaseModel
from karpyncho.pydantic_extensions import DateDMYSerializerMixin

class Person(DateDMYSerializerMixin, BaseModel):
    name: str
    birth_date: date
    
# This will raise a validation error
try:
    person = Person(name="John Doe", birth_date="2000-01-01")  # Wrong format
except ValueError as e:
    print(f"Error: {e}")  # Error: Date must be in %d/%m/%Y format
```

## How It Works

The mixins utilize Pydantic's initialization hooks and field validators to:

1. Detect all date fields automatically
2. Validate and convert string inputs to date objects
3. Serialize date objects to strings in the specified format
4. Override the `model_dump` method to ensure consistent formatting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
