import json

from datetime import date
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
        data = MyDataClass(str_field="Hola", date_field=date(2023, 1, 3))
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
        data = MyDataDMYClass(str_field="Hola", date_field=date(2023, 1, 3))
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
        data = MyDataNumberClass(str_field="Hola", date_field=date(2023, 1, 3))
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
