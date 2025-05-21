"""
pydantic_extensions

This package provides extensions and enhancements to the Pydantic library,
offering custom mixins for handling date serialization in various formats.

Key Features:
- `DateSerializerMixin`: A mixin for handling dates with a customizable format.
- `DateDMYSerializerMixin`: A specific mixin for handling dates in DD/MM/YYYY format.
- Validators for converting string dates to date objects.

Usage:
Import the necessary components from the package to extend your Pydantic models
and leverage additional functionalities.

Example:
    from karpyncho.pydantic_extensions import DateSerializerMixin, DateDMYSerializerMixin

"""
from datetime import date, datetime
from typing import Any, ClassVar, Optional

from pydantic import ConfigDict, field_validator


class DateSerializerMixin:
    """
    Generic mixin for handling dates with custom format in Pydantic models.
    it will accept optionals 0s in day and month both (2023-01-05) and (2023-1-5) are
    valid dates

    """

    # Class variables
    __date_fields__: ClassVar[set] = set()
    __date_format__: ClassVar[str] = "%Y-%m-%d"  # Default ISO format

    # Empty config to start with
    model_config = ConfigDict()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        """Collect all date fields when subclass is initialized."""
        super().__pydantic_init_subclass__(**kwargs)

        # Collect date fields
        for field_name, field_info in cls.model_fields.items():
            if field_info.annotation in {date, Optional[date]}:
                cls.__date_fields__.add(field_name)

        # Update the model_config with json_encoders for date formatting
        cls.model_config = ConfigDict(
            json_encoders={date: lambda d: d.strftime(cls.__date_format__)}
        )

    @field_validator('*', mode='before')
    @classmethod
    def validate_date_format(cls, v: Any, info):
        """Convert string dates in the specified format to date objects."""
        if info.field_name in cls.__date_fields__ and isinstance(v, str):
            if v == '':
                return None
            try:
                return datetime.strptime(v, cls.__date_format__).date()
            except ValueError as e:
                raise ValueError(f'Date must be in {cls.__date_format__} format: {e}') from e
        return v

    def model_dump(self, **kwargs):
        """Override model_dump to format dates according to __date_format__."""
        data = super().model_dump(**kwargs)
        for field_name in self.__date_fields__:
            if field_name in data and isinstance(data[field_name], date):
                data[field_name] = data[field_name].strftime(self.__date_format__)
        return data


class DateDMYSerializerMixin(DateSerializerMixin):
    """
    Specific mixin for handling dates in DD/MM/YYYY format in Pydantic models.
    it will accept optionals 0s in day and month both (05/01/2023) and (5/1/2023) are
    valid dates
    """

    # Only override the date format
    __date_format__: ClassVar[str] = "%d/%m/%Y"


class DateNumberSerializerMixin(DateSerializerMixin):
    """
    Mixin for handling date serialization in 'YYYYMMDD' format in Pydantic models.

    This mixin extends the DateSerializerMixin to validate and convert dates
    represented as integers in the 'YYYYMMDD' format to date objects.
    examples of valid fields are '20230512' and '20230508'.

    Fields:
        __date_format__: ClassVar[str] = '%Y%m%d'
    """

    # Only override the date format
    __date_format__: ClassVar[str] = "%Y%m%d"

    @field_validator('*', mode='before')
    @classmethod
    def validate_date_format(cls, v: Any, info):
        """Convert string dates in the specified format to date objects."""
        if info.field_name in cls.__date_fields__ and isinstance(v, int):
            if v == 0:
                return None
            try:
                return datetime.strptime(str(v), cls.__date_format__).date()
            except ValueError as e:
                raise ValueError(f'Date must be in {cls.__date_format__} format: {e}') from e
        return v

    def model_dump(self, **kwargs):
        """Override model_dump to format dates according to __date_format__."""
        data = super().model_dump(**kwargs)  # this line is converting all dates fields to str
        for field_name in self.__date_fields__:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = int(getattr(self, field_name).strftime(self.__date_format__))
        return data
