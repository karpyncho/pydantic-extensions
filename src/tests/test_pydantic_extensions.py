import json

from datetime import date
from typing import Annotated
from unittest import TestCase

from pydantic import BaseModel

from karpyncho.pydantic_extensions import DateDMYSerializerMixin
from karpyncho.pydantic_extensions import DateNumberSerializerMixin
from karpyncho.pydantic_extensions import DateSerializerMixin
from karpyncho.pydantic_extensions import DateFormat
from karpyncho.pydantic_extensions import ISO_FORMAT
from karpyncho.pydantic_extensions import DMY_FORMAT
from karpyncho.pydantic_extensions import MDY_FORMAT
from karpyncho.pydantic_extensions import NUMBER_FORMAT


class MyDataClass(DateSerializerMixin, BaseModel):
    str_field: str
    date_field: date


class MyDataOptionalClass(DateSerializerMixin, BaseModel):
    str_field: str
    date_field: date
    optional_date_field: date | None


class MyDataDMYClass(DateDMYSerializerMixin, BaseModel):
    str_field: str
    date_field: date


class MyDataNumberClass(DateNumberSerializerMixin, BaseModel):
    str_field: str
    date_field: date


class MyDataNumberOptionalClass(DateNumberSerializerMixin, BaseModel):
    str_field: str
    date_field: date
    optional_date_field: date | None


class DateSerializerMixinTest(TestCase):
    def test_date_serializer_mixin_serialize(self) -> None:
        data = MyDataClass(str_field="Hola", date_field=date(2023, 1, 3))  # type: ignore[arg-type]
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": "2023-01-03"}
        )

    def test_date_serializer_mixin_deserialize(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "2019-05-23"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_serializer_mixin_deserialize_value_error(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataClass(**my_dict)

    def test_date_dmy_serializer_mixin_deserialize_one_digit_month(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "2019-5-3"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_0_digit_day(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "2019-5-03"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_two_digit_year(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "19-05-03"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataClass(**my_dict)

    def test_date_serializer_mixin_deserialize_optional_empty(self) -> None:
        json_raw = """{
            "str_field": "hola",
            "date_field": "2019-5-03",
            "optional_date_field": ""
        }"""
        my_dict = json.loads(json_raw)
        obj = MyDataOptionalClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))
        self.assertIsNone(obj.optional_date_field)


class DateDMYSerializerMixinTest(TestCase):
    def test_date_dmy_serializer_mixin_serialize(self) -> None:
        data = MyDataDMYClass(str_field="Hola", date_field=date(2023, 1, 3))  # type: ignore[arg-type]
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": "03/01/2023"}
        )

    def test_date_dmy_serializer_mixin_deserialize(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "23/05/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_dmy_serializer_mixin_deserialize_one_digit_month(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "3/5/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_0_padded_day(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "03/5/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_two_digit_year(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "03/5/19"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataDMYClass(**my_dict)

    def test_date_dmy_serializer_mixin_deserialize_value_error(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)

        with self.assertRaises(ValueError):
            MyDataDMYClass(**my_dict)


class DateNumberSerializerMixinTest(TestCase):

    def test_date_number_serializer_mixin_serialize(self) -> None:
        data = MyDataNumberClass(str_field="Hola", date_field=date(2023, 1, 3))  # type: ignore[arg-type]
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": 20230103}
        )

    def test_date_number_serializer_mixin_deserialize(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": 20190523}'
        my_dict = json.loads(json_raw)
        obj = MyDataNumberClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_number_serializer_mixin_deserialize_one_digit_month(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": 20190503}'
        my_dict = json.loads(json_raw)
        obj = MyDataNumberClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_number_serializer_mixin_deserialize_two_digit_year(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": 1905003}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataNumberClass(**my_dict)

    def test_date_number_serializer_mixin_deserialize_value_error(self) -> None:
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)

        with self.assertRaises(ValueError):
            MyDataNumberClass(**my_dict)

    def test_date_number_serializer_mixin_deserialize_optional_empty(self) -> None:
        json_raw = """
        {
            "str_field": "hola",
            "date_field": 20190503,
            "optional_date_field": 0
        }
        """
        my_dict = json.loads(json_raw)
        obj = MyDataNumberOptionalClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))
        self.assertIsNone(obj.optional_date_field)


class DateFormatTest(TestCase):
    """Tests for DateFormat class and predefined constants."""

    def test_date_format_creation(self) -> None:
        """Test DateFormat can be created with a format string."""
        fmt = DateFormat("%Y-%m-%d")
        self.assertEqual(fmt.format, "%Y-%m-%d")

    def test_date_format_str(self) -> None:
        """Test DateFormat __str__ returns format string."""
        fmt = DateFormat("%d/%m/%Y")
        self.assertEqual(str(fmt), "%d/%m/%Y")

    def test_date_format_repr(self) -> None:
        """Test DateFormat __repr__ returns proper representation."""
        fmt = DateFormat("%Y%m%d")
        self.assertEqual(repr(fmt), "DateFormat('%Y%m%d')")

    def test_date_format_equality(self) -> None:
        """Test DateFormat equality comparison."""
        fmt1 = DateFormat("%Y-%m-%d")
        fmt2 = DateFormat("%Y-%m-%d")
        fmt3 = DateFormat("%d/%m/%Y")
        self.assertEqual(fmt1, fmt2)
        self.assertNotEqual(fmt1, fmt3)

    def test_date_format_equality_with_other_types(self) -> None:
        """Test DateFormat inequality with non-DateFormat objects."""
        fmt = DateFormat("%Y-%m-%d")
        self.assertNotEqual(fmt, "%Y-%m-%d")
        self.assertNotEqual(fmt, None)
        self.assertNotEqual(fmt, 123)

    def test_date_format_equality_with_iso_format(self) -> None:
        """Test DateFormat equality with predefined constants."""
        fmt = DateFormat("%Y-%m-%d")
        self.assertEqual(fmt, ISO_FORMAT)

    def test_date_format_hash(self) -> None:
        """Test DateFormat is hashable."""
        fmt1 = DateFormat("%Y-%m-%d")
        fmt2 = DateFormat("%Y-%m-%d")
        self.assertEqual(hash(fmt1), hash(fmt2))

    def test_iso_format_constant(self) -> None:
        """Test ISO_FORMAT constant."""
        self.assertEqual(ISO_FORMAT.format, "%Y-%m-%d")

    def test_dmy_format_constant(self) -> None:
        """Test DMY_FORMAT constant."""
        self.assertEqual(DMY_FORMAT.format, "%d/%m/%Y")

    def test_mdy_format_constant(self) -> None:
        """Test MDY_FORMAT constant."""
        self.assertEqual(MDY_FORMAT.format, "%m/%d/%Y")

    def test_number_format_constant(self) -> None:
        """Test NUMBER_FORMAT constant."""
        self.assertEqual(NUMBER_FORMAT.format, "%Y%m%d")

    def test_mixin_with_iso_format_constant(self) -> None:
        """Test using ISO_FORMAT constant with DateSerializerMixin."""

        class PersonISO(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: date

        person = PersonISO(name="John", birth_date="2000-01-21")  # type: ignore
        self.assertEqual(
            person.model_dump(), {"name": "John", "birth_date": "2000-01-21"}
        )

    def test_mixin_with_dmy_format_constant(self) -> None:
        """Test using DMY_FORMAT constant with DateSerializerMixin."""

        class PersonDMY(DateSerializerMixin, BaseModel):
            __date_format__ = DMY_FORMAT
            name: str
            birth_date: date

        person = PersonDMY(name="Jane", birth_date="21/01/2000")  # type: ignore
        self.assertEqual(
            person.model_dump(), {"name": "Jane", "birth_date": "21/01/2000"}
        )

    def test_mixin_with_mdy_format_constant(self) -> None:
        """Test using MDY_FORMAT constant (American format)."""

        class PersonMDY(DateSerializerMixin, BaseModel):
            __date_format__ = MDY_FORMAT
            name: str
            birth_date: date

        person = PersonMDY(name="Bob", birth_date="01/21/2000")  # type: ignore
        self.assertEqual(
            person.model_dump(), {"name": "Bob", "birth_date": "01/21/2000"}
        )

    def test_mixin_with_number_format_constant(self) -> None:
        """Test using NUMBER_FORMAT constant with DateNumberSerializerMixin."""

        class TransactionNum(DateNumberSerializerMixin, BaseModel):
            __date_format__ = NUMBER_FORMAT
            transaction_id: str
            transaction_date: date

        trans = TransactionNum(transaction_id="TXN001", transaction_date=20230512)  # type: ignore
        self.assertEqual(
            trans.model_dump(),
            {"transaction_id": "TXN001", "transaction_date": 20230512},
        )

    def test_custom_date_format(self) -> None:
        """Test creating and using custom DateFormat."""
        custom_format = DateFormat("%d-%m-%Y")

        class PersonCustom(DateSerializerMixin, BaseModel):
            __date_format__ = custom_format
            name: str
            birth_date: date

        person = PersonCustom(name="Alice", birth_date="15-03-1990")  # type: ignore
        self.assertEqual(
            person.model_dump(), {"name": "Alice", "birth_date": "15-03-1990"}
        )

    def test_dmy_serializer_mixin_uses_dmy_format(self) -> None:
        """Test that DateDMYSerializerMixin uses DMY_FORMAT internally."""

        class PersonDMYMixin(DateDMYSerializerMixin, BaseModel):
            name: str
            birth_date: date

        person = PersonDMYMixin(name="Charlie", birth_date="10/05/2000")  # type: ignore
        self.assertEqual(
            person.model_dump(), {"name": "Charlie", "birth_date": "10/05/2000"}
        )

    def test_date_format_pydantic_core_schema(self) -> None:
        """Test DateFormat __get_pydantic_core_schema__ method."""
        fmt = DateFormat("%Y-%m-%d")
        # Create a mock handler
        class MockHandler:
            def __call__(self, type_):
                # Return a simple schema for testing
                from pydantic_core import core_schema
                return core_schema.date_schema()

        handler = MockHandler()
        schema = fmt.__get_pydantic_core_schema__(date, handler)  # type: ignore
        # Verify the schema is a CoreSchema object
        self.assertIsNotNone(schema)


class FlexibleDateFormatTest(TestCase):
    """Tests for per-field date format annotation support."""

    def test_annotated_field_with_dmy_format(self) -> None:
        """Test field with Annotated[date, DMY_FORMAT] uses correct format."""

        class Person(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: Annotated[date, DMY_FORMAT]

        person = Person(name="John", birth_date="21/01/2000")  # type: ignore
        self.assertEqual(person.birth_date, date(2000, 1, 21))
        self.assertEqual(
            person.model_dump(),
            {"name": "John", "birth_date": "21/01/2000"},
        )

    def test_mixed_formats_in_same_model(self) -> None:
        """Test model with fields using different formats."""

        class Event(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            start_date: date
            end_date: Annotated[date, DMY_FORMAT]
            registration_date: Annotated[date, MDY_FORMAT]

        event = Event(  # type: ignore[call-arg]
            name="Conference",
            start_date="2023-06-01",  # type: ignore[arg-type]  # ISO format
            end_date="05/06/2023",  # type: ignore[arg-type]  # DMY format
            registration_date="01/03/2023",  # type: ignore[arg-type]  # MDY format
        )

        self.assertEqual(event.start_date, date(2023, 6, 1))
        self.assertEqual(event.end_date, date(2023, 6, 5))
        self.assertEqual(event.registration_date, date(2023, 1, 3))

        dumped = event.model_dump()
        self.assertEqual(dumped["start_date"], "2023-06-01")  # ISO
        self.assertEqual(dumped["end_date"], "05/06/2023")  # DMY
        self.assertEqual(dumped["registration_date"], "01/03/2023")  # MDY

    def test_custom_format_with_annotated(self) -> None:
        """Test using custom DateFormat with Annotated."""

        custom_format = DateFormat("%d-%m-%Y")

        class Person(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: Annotated[date, custom_format]

        person = Person(name="Alice", birth_date="15-03-1990")  # type: ignore
        self.assertEqual(person.birth_date, date(1990, 3, 15))
        self.assertEqual(
            person.model_dump(),
            {"name": "Alice", "birth_date": "15-03-1990"},
        )

    def test_optional_annotated_field(self) -> None:
        """Test optional field with Annotated format."""

        class Application(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            application_date: date
            approval_date: Annotated[date | None, DMY_FORMAT] = None

        # With approval date
        app1 = Application(  # type: ignore
            name="John",
            application_date="2024-03-15",  # type: ignore[arg-type]
            approval_date="20/03/2024",  # type: ignore[arg-type]
        )
        self.assertEqual(app1.approval_date, date(2024, 3, 20))
        self.assertEqual(app1.model_dump()["approval_date"], "20/03/2024")

        # Without approval date (omitted field)
        app2 = Application(  # type: ignore
            name="Jane", application_date="2024-03-15"  # type: ignore[arg-type]
        )
        self.assertIsNone(app2.approval_date)

    def test_annotated_with_number_serializer(self) -> None:
        """Test Annotated formats with DateNumberSerializerMixin."""

        class Transaction(DateNumberSerializerMixin, BaseModel):
            __date_format__ = NUMBER_FORMAT
            transaction_id: str
            transaction_date: date
            approval_date: Annotated[date, DMY_FORMAT]

        trans = Transaction(  # type: ignore
            transaction_id="TXN001",
            transaction_date=20231225,  # type: ignore[arg-type]
            approval_date="25/12/2023",  # type: ignore[arg-type]
        )

        self.assertEqual(trans.transaction_date, date(2023, 12, 25))
        self.assertEqual(trans.approval_date, date(2023, 12, 25))

        dumped = trans.model_dump()
        # transaction_date should be integer (numeric format)
        self.assertEqual(dumped["transaction_date"], 20231225)
        # approval_date should be string (DMY format)
        self.assertEqual(dumped["approval_date"], "25/12/2023")

    def test_annotated_with_dmy_serializer(self) -> None:
        """Test Annotated formats with DateDMYSerializerMixin."""

        class Document(DateDMYSerializerMixin, BaseModel):
            title: str
            created_date: date
            updated_date: Annotated[date, ISO_FORMAT]

        doc = Document(  # type: ignore
            title="Report",
            created_date="15/03/2024",  # type: ignore[arg-type]
            updated_date="2024-03-20",  # type: ignore[arg-type]
        )

        dumped = doc.model_dump()
        self.assertEqual(dumped["created_date"], "15/03/2024")  # DMY (default)
        self.assertEqual(dumped["updated_date"], "2024-03-20")  # ISO (annotated)

    def test_deserialization_with_annotated_formats(self) -> None:
        """Test JSON deserialization with annotated formats."""

        class Person(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: Annotated[date, DMY_FORMAT]

        json_raw = '{"name": "Bob", "birth_date": "10/05/2000"}'
        my_dict = json.loads(json_raw)
        person = Person(**my_dict)

        self.assertEqual(person.name, "Bob")
        self.assertEqual(person.birth_date, date(2000, 5, 10))

    def test_annotated_field_wrong_format_error(self) -> None:
        """Test validation error when using wrong format for annotated field."""

        class Person(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: Annotated[date, DMY_FORMAT]

        with self.assertRaises(ValueError):
            Person(  # type: ignore[call-arg]
                name="Charlie", birth_date="2000-05-10"  # type: ignore[arg-type]
            )  # ISO format, but DMY expected

    def test_multiple_annotated_fields_same_format(self) -> None:
        """Test multiple annotated fields using the same custom format."""

        custom_fmt = DateFormat("%Y/%m/%d")

        class Report(DateSerializerMixin, BaseModel):
            __date_format__ = DMY_FORMAT
            title: str
            start_date: Annotated[date, custom_fmt]
            end_date: Annotated[date, custom_fmt]
            created_date: date  # Uses default DMY format

        report = Report(  # type: ignore[call-arg]
            title="Q1 Report",
            start_date="2024/01/01",  # type: ignore[arg-type]
            end_date="2024/03/31",  # type: ignore[arg-type]
            created_date="15/04/2024",  # type: ignore[arg-type]
        )

        dumped = report.model_dump()
        self.assertEqual(dumped["start_date"], "2024/01/01")
        self.assertEqual(dumped["end_date"], "2024/03/31")
        self.assertEqual(dumped["created_date"], "15/04/2024")

    def test_annotated_with_number_mixed_fields(self) -> None:
        """Test NumberSerializer with mix of numeric and string formats."""

        class MixedDates(DateNumberSerializerMixin, BaseModel):
            __date_format__ = NUMBER_FORMAT
            numeric_date: date
            string_date: Annotated[date, DMY_FORMAT]

        obj = MixedDates(  # type: ignore[call-arg]
            numeric_date=20240315,  # type: ignore[arg-type]
            string_date="15/03/2024",  # type: ignore[arg-type]
        )

        dumped = obj.model_dump()
        # numeric_date should be integer
        self.assertEqual(dumped["numeric_date"], 20240315)
        # string_date should be string
        self.assertEqual(dumped["string_date"], "15/03/2024")


class EdgeCaseCoverageTest(TestCase):
    """Tests for edge cases to achieve 100% coverage."""

    def test_get_date_format_from_metadata_without_date_format(self) -> None:
        """Test _get_date_format_from_metadata returns default when no DateFormat in metadata."""

        class Person(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            # Field with metadata but no DateFormat object
            birth_date: Annotated[date, "some string annotation"]

        person = Person(name="John", birth_date="2000-01-21")  # type: ignore
        # Should use default format (ISO_FORMAT)
        self.assertEqual(
            person.model_dump(),
            {"name": "John", "birth_date": "2000-01-21"},
        )

    def test_is_date_field_with_union_types(self) -> None:
        """Test _is_date_field properly detects date in union types."""

        class PersonOptional(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            birth_date: date | None

        # Test with None
        person1 = PersonOptional(name="John", birth_date=None)  # type: ignore
        self.assertIsNone(person1.birth_date)

        # Test with date
        person2 = PersonOptional(name="Jane", birth_date="2000-01-21")  # type: ignore
        self.assertEqual(person2.birth_date, date(2000, 1, 21))

    def test_date_number_serializer_mixin_empty_string_optional(self) -> None:
        """Test DateNumberSerializerMixin handles empty string for optional fields."""

        class Transaction(DateNumberSerializerMixin, BaseModel):
            transaction_id: str
            transaction_date: date
            optional_date: date | None = None

        trans = Transaction(
            transaction_id="TXN001",
            transaction_date=20231225,  # type: ignore[arg-type]
            optional_date="",  # type: ignore[arg-type]
        )
        self.assertIsNone(trans.optional_date)

    def test_date_number_serializer_mixin_string_value_error(self) -> None:
        """Test DateNumberSerializerMixin raises error for invalid string date."""

        class Transaction(DateNumberSerializerMixin, BaseModel):
            transaction_id: str
            transaction_date: date
            string_date: Annotated[date, DMY_FORMAT]

        with self.assertRaises(ValueError):
            Transaction(
                transaction_id="TXN001",
                transaction_date=20231225,  # type: ignore[arg-type]
                string_date="INVALID/DATE/STRING",  # type: ignore[arg-type]
            )

    def test_annotated_field_without_metadata(self) -> None:
        """Test Annotated field without format metadata uses default format."""

        class Document(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            title: str
            created_date: Annotated[date, "just a string"]

        doc = Document(title="Test", created_date="2024-01-15")  # type: ignore
        self.assertEqual(
            doc.model_dump(),
            {"title": "Test", "created_date": "2024-01-15"},
        )

    def test_date_number_serializer_with_annotated_string_format(self) -> None:
        """Test DateNumberSerializerMixin with annotated string format field."""

        class Transaction(DateNumberSerializerMixin, BaseModel):
            transaction_id: str
            numeric_date: date
            string_date: Annotated[date, DMY_FORMAT]

        trans = Transaction(
            transaction_id="TXN001",
            numeric_date=20231225,  # type: ignore[arg-type]
            string_date="25/12/2023",  # type: ignore[arg-type]
        )
        # String field should be parsed as string, not as numeric
        self.assertEqual(trans.string_date, date(2023, 12, 25))
        dumped = trans.model_dump()
        self.assertEqual(dumped["string_date"], "25/12/2023")

    def test_directly_test_is_date_field_method(self) -> None:
        """Test _is_date_field method with various union type annotations."""

        # Direct test of the _is_date_field method
        # This tests the code path for union type detection
        self.assertTrue(DateSerializerMixin._is_date_field(date))
        self.assertTrue(DateSerializerMixin._is_date_field(date | None))

        # Test with non-date types
        self.assertFalse(DateSerializerMixin._is_date_field(str))
        self.assertFalse(DateSerializerMixin._is_date_field(int))
        self.assertFalse(DateSerializerMixin._is_date_field(str | None))

    def test_test_optional_date_with_model(self) -> None:
        """Test that optional date fields are properly detected and handled."""

        class OptionalEvent(DateSerializerMixin, BaseModel):
            __date_format__ = ISO_FORMAT
            name: str
            event_date: date | None = None
            other_date: date | None

        # Test with explicit None
        event1 = OptionalEvent(name="Test", event_date=None, other_date=None)
        self.assertIsNone(event1.event_date)
        self.assertIsNone(event1.other_date)

        # Test with date values
        event2 = OptionalEvent(
            name="Test",
            event_date="2024-01-15",  # type: ignore[arg-type]
            other_date="2024-02-20",  # type: ignore[arg-type]
        )
        self.assertEqual(event2.event_date, date(2024, 1, 15))
        self.assertEqual(event2.other_date, date(2024, 2, 20))

    def test_is_date_field_with_annotated(self) -> None:
        """Test _is_date_field method with Annotated types."""
        # Test with Annotated[date, format]
        annotation = Annotated[date, DMY_FORMAT]
        self.assertTrue(DateSerializerMixin._is_date_field(annotation))
