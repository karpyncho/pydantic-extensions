"""
pydantic_extensions

This package provides extensions and enhancements to the Pydantic library,
offering custom mixins for handling date serialization in various formats.

Key Features:
- `DateSerializerMixin`: A mixin for handling dates with a customizable format.
- `DateDMYSerializerMixin`: A specific mixin for handling dates in DD/MM/YYYY format.
- `DateNumberSerializerMixin`: A mixin for handling dates in YYYYMMDD integer format.
- Predefined date format constants for convenience.
- Validators for converting string dates to date objects.

Usage:
Import the necessary components from the package to extend your Pydantic models
and leverage additional functionalities.

Example:
    from karpyncho.pydantic_extensions import (
        DateSerializerMixin,
        DateDMYSerializerMixin,
        DateNumberSerializerMixin,
        ISO_FORMAT,
        DMY_FORMAT,
    )

"""
from datetime import date
from datetime import datetime
from typing import Annotated
from typing import Any
from typing import ClassVar
from typing import Protocol
from typing import cast
from typing import get_args
from typing import get_origin
from typing import runtime_checkable

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import GetCoreSchemaHandler
from pydantic import field_validator
from pydantic.fields import FieldInfo

from pydantic_core import core_schema

# Export public API
__all__ = [
    "Annotated",
    "DateFormat",
    "DateSerializerMixin",
    "DateDMYSerializerMixin",
    "DateNumberSerializerMixin",
    "ISO_FORMAT",
    "DMY_FORMAT",
    "MDY_FORMAT",
    "NUMBER_FORMAT",
    "PydanticModelProtocol",
]


class DateFormat:
    """
    Represents a date format specification for use with date serialization mixins.

    This class provides a convenient way to define and document date formats
    used throughout your Pydantic models.

    Args:
        format_str: The strftime format string for date serialization/deserialization

    Attributes:
        format: The strftime format string

    Example:
        >>> custom_format = DateFormat("%d/%m/%Y")
        >>> custom_format.format
        '%d/%m/%Y'
    """

    def __init__(self, format_str: str) -> None:
        """Initialize a DateFormat with a strftime format string."""
        self.format = format_str

    def __str__(self) -> str:
        """Return the format string representation."""
        return self.format

    def __repr__(self) -> str:
        """Return a detailed representation of the DateFormat."""
        return f"DateFormat('{self.format}')"

    def __eq__(self, other: object) -> bool:
        """Check equality based on format string."""
        if isinstance(other, DateFormat):
            return self.format == other.format
        return False

    def __hash__(self) -> int:
        """Make DateFormat hashable."""
        return hash(self.format)

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler  # pylint: disable=unused-argument
    ) -> core_schema.CoreSchema:
        """Handle the schema generation for Pydantic."""
        return core_schema.no_info_after_validator_function(
            lambda x: x,
            handler(date)
        )


# Pre-defined format markers for convenience
ISO_FORMAT = DateFormat("%Y-%m-%d")
"""ISO 8601 date format: YYYY-MM-DD"""

DMY_FORMAT = DateFormat("%d/%m/%Y")
"""European date format: DD/MM/YYYY"""

MDY_FORMAT = DateFormat("%m/%d/%Y")
"""American date format: MM/DD/YYYY"""

NUMBER_FORMAT = DateFormat("%Y%m%d")
"""Numeric date format: YYYYMMDD (for integer serialization)"""


@runtime_checkable
class PydanticModelProtocol(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol defining the Pydantic interface our mixin expects."""
    model_fields: ClassVar[dict[str, FieldInfo]]
    model_config: ConfigDict

    # pylint: disable=missing-function-docstring
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None: ...
    def model_dump(self, **kwargs: Any) -> dict[str, Any]: ...


class DateSerializerMixin:
    """
    Generic mixin for handling dates with custom format in Pydantic models.

    It will accept optional leading zeros in day and month, so both
    (2023-01-05) and (2023-1-5) are valid dates.

    You can specify the date format using either:
    - A string: __date_format__ = "%Y-%m-%d"
    - A DateFormat constant: __date_format__ = ISO_FORMAT

    For per-field formats, use Annotated:
    - birth_date: Annotated[date, DMY_FORMAT]
    - created_at: Annotated[date, DateFormat("%Y/%m/%d")]

    Attributes:
        __date_format__: ClassVar - Default date format (default: ISO_FORMAT)
        __date_fields__: ClassVar - Set of date field names
        __date_fields_config__: ClassVar - Dict mapping field names to formats

    Example:
        >>> from datetime import date
        >>> from pydantic import BaseModel
        >>> from typing import Annotated
        >>> from karpyncho.pydantic_extensions import DateSerializerMixin, ISO_FORMAT, DMY_FORMAT
        >>> class Person(DateSerializerMixin, BaseModel):
        ...     __date_format__ = ISO_FORMAT
        ...     name: str
        ...     birth_date: Annotated[date, DMY_FORMAT]  # Uses DD/MM/YYYY
        ...     created_at: date  # Uses default ISO format
    """

    # Class variables
    __date_fields__: ClassVar[set] = set()
    __date_fields_config__: ClassVar[dict[str, str]] = {}
    __date_format__: ClassVar[str | DateFormat] = "%Y-%m-%d"  # Default ISO format

    # Empty config to start with
    model_config = ConfigDict()

    @classmethod
    def _get_date_format_from_metadata(cls, field_info, default_format):
        """Extract format from field metadata, return default if not found."""
        if not field_info.metadata:
            return default_format
        for metadata in field_info.metadata:
            if isinstance(metadata, DateFormat):
                return str(metadata)
        return default_format

    @classmethod
    def _is_date_field(cls, annotation):
        """Check if annotation represents a date field."""
        if annotation is date or annotation == date | None:
            return True
        origin = get_origin(annotation)
        if origin is Annotated:
            args = get_args(annotation)
            return date in args
        if origin in (type(date | None), type(None)):
            args = get_args(annotation)
            return date in args or any(
                arg is date for arg in args if arg is not type(None)  # pylint: disable=unidiomatic-typecheck
            )
        return False

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        """Collect all date fields and their formats when subclass is initialized."""
        pydantic_cls = cast("type[PydanticModelProtocol]", cls)
        cast(BaseModel, super()).__pydantic_init_subclass__(**kwargs)  # noqa: TC006

        # Reset class variables for each subclass
        cls.__date_fields__ = set()
        cls.__date_fields_config__ = {}
        default_format_str = str(cls.__date_format__)

        # Collect date fields and their specific formats
        for field_name, field_info in pydantic_cls.model_fields.items():
            if cls._is_date_field(field_info.annotation):
                cls.__date_fields__.add(field_name)
                field_format = cls._get_date_format_from_metadata(
                    field_info, default_format_str
                )
                cls.__date_fields_config__[field_name] = field_format

        # Update the model_config with json_encoders for date formatting
        cls.model_config = ConfigDict(
            json_encoders={date: lambda d: d.strftime(default_format_str)}
        )

    @field_validator("*", mode="before")
    @classmethod
    def validate_date_format(cls, v: Any, info):
        """Convert string dates in the specified format to date objects."""
        if info.field_name in cls.__date_fields_config__:
            if v is None or v == "":
                return None

            date_format_str = cls.__date_fields_config__[info.field_name]

            if isinstance(v, str):
                try:
                    return datetime.strptime(v, date_format_str).date()
                except ValueError as e:
                    error_msg = f"Date must be in {date_format_str} format: {e}"
                    raise ValueError(error_msg) from e
        return v

    def model_dump(self, **kwargs):
        """Override model_dump to format dates according to their specific formats."""
        data = cast("BaseModel", super()).model_dump(**kwargs)
        for field_name, date_format_str in self.__date_fields_config__.items():
            if field_name in data and isinstance(data[field_name], date):
                data[field_name] = data[field_name].strftime(date_format_str)
        return data


class DateDMYSerializerMixin(DateSerializerMixin):
    """
    Specific mixin for handling dates in DD/MM/YYYY (European) format in Pydantic models.

    It will accept optional leading zeros in day and month, so both
    (05/01/2023) and (5/1/2023) are valid dates.

    This mixin is equivalent to:
        class MyModel(DateSerializerMixin, BaseModel):
            __date_format__ = DMY_FORMAT

    Example:
        >>> from datetime import date
        >>> from pydantic import BaseModel
        >>> from karpyncho.pydantic_extensions import DateDMYSerializerMixin
        >>> class Person(DateDMYSerializerMixin, BaseModel):
        ...     name: str
        ...     birth_date: date
        >>> person = Person(name="John", birth_date="21/01/2000")
    """

    # Only override the date format
    __date_format__: ClassVar[str | DateFormat] = DMY_FORMAT


class DateNumberSerializerMixin(DateSerializerMixin):
    """
    Mixin for handling date serialization in YYYYMMDD (numeric) format in Pydantic models.

    This mixin extends the DateSerializerMixin to validate and convert dates
    represented as integers in the YYYYMMDD format to date objects.

    Valid input examples: 20230512, 20230508
    Input is expected as integers and output will be serialized as integers.

    This mixin is equivalent to:
        class MyModel(DateSerializerMixin, BaseModel):
            __date_format__ = NUMBER_FORMAT

    Attributes:
        __date_format__: ClassVar[str | DateFormat] = NUMBER_FORMAT ('%Y%m%d')

    Example:
        >>> from datetime import date
        >>> from pydantic import BaseModel
        >>> from karpyncho.pydantic_extensions import DateNumberSerializerMixin
        >>> class Transaction(DateNumberSerializerMixin, BaseModel):
        ...     transaction_id: str
        ...     transaction_date: date
        >>> trans = Transaction(transaction_id="TXN001", transaction_date=20231225)
    """

    # Only override the date format
    __date_format__: ClassVar[str | DateFormat] = NUMBER_FORMAT
    __numeric_fields__: ClassVar[set] = set()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        """Initialize and mark which fields use numeric format."""
        super().__pydantic_init_subclass__(**kwargs)
        # Track which fields are numeric (have %Y%m%d or similar patterns without separators)
        cls.__numeric_fields__ = set()
        for field_name, field_format in cls.__date_fields_config__.items():
            # Check if format is numeric (no separators like -, /, etc.)
            if all(c not in field_format for c in ["/", "-", "."]):
                cls.__numeric_fields__.add(field_name)

    @field_validator("*", mode="before")
    @classmethod
    def validate_date_format(cls, v: Any, info):
        """Convert dates in their respective formats to date objects."""
        if info.field_name not in cls.__date_fields_config__:
            return v

        if v is None or v == "":
            return None

        date_format_str = cls.__date_fields_config__[info.field_name]

        # Check if this field uses numeric format
        if info.field_name in cls.__numeric_fields__:
            if isinstance(v, int):
                if v == 0:
                    return None
                try:
                    return datetime.strptime(str(v), date_format_str).date()
                except ValueError as e:
                    error_msg = f"Date must be in {date_format_str} format: {e}"
                    raise ValueError(error_msg) from e
        # For non-numeric fields, process strings
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, date_format_str).date()
            except ValueError as e:
                error_msg = f"Date must be in {date_format_str} format: {e}"
                raise ValueError(error_msg) from e
        return v

    def model_dump(self, **kwargs):
        """Override model_dump to format dates as integers according to their format."""
        # Call parent's model_dump which converts dates to strings
        data = super().model_dump(**kwargs)
        for field_name in self.__numeric_fields__:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = int(data[field_name])
        return data
