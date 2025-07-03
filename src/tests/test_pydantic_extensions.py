import json

from datetime import date
from unittest import TestCase

from pydantic import BaseModel

from karpyncho.pydantic_extensions import DateDMYSerializerMixin
from karpyncho.pydantic_extensions import DateNumberSerializerMixin
from karpyncho.pydantic_extensions import DateSerializerMixin


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
    def test_date_serializer_mixin_serialize(self):
        data = MyDataClass(str_field="Hola", date_field=date(2023, 1, 3))
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": "2023-01-03"}
        )

    def test_date_serializer_mixin_deserialize(self):
        json_raw = '{"str_field": "hola", "date_field": "2019-05-23"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_serializer_mixin_deserialize_value_error(self):
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataClass(**my_dict)

    def test_date_dmy_serializer_mixin_deserialize_one_digit_month(self):
        json_raw = '{"str_field": "hola", "date_field": "2019-5-3"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_0_digit_day(self):
        json_raw = '{"str_field": "hola", "date_field": "2019-5-03"}'
        my_dict = json.loads(json_raw)
        obj = MyDataClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_two_digit_year(self):
        json_raw = '{"str_field": "hola", "date_field": "19-05-03"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataClass(**my_dict)

    def test_date_serializer_mixin_deserialize_optional_empty(self):
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
    def test_date_dmy_serializer_mixin_serialize(self):
        data = MyDataDMYClass(str_field="Hola", date_field=date(2023, 1, 3))
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": "03/01/2023"}
        )

    def test_date_dmy_serializer_mixin_deserialize(self):
        json_raw = '{"str_field": "hola", "date_field": "23/05/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_dmy_serializer_mixin_deserialize_one_digit_month(self):
        json_raw = '{"str_field": "hola", "date_field": "3/5/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_0_padded_day(self):
        json_raw = '{"str_field": "hola", "date_field": "03/5/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_dmy_serializer_mixin_deserialize_two_digit_year(self):
        json_raw = '{"str_field": "hola", "date_field": "03/5/19"}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataDMYClass(**my_dict)

    def test_date_dmy_serializer_mixin_deserialize_value_error(self):
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)

        with self.assertRaises(ValueError):
            MyDataDMYClass(**my_dict)


class DateNumberSerializerMixinTest(TestCase):

    def test_date_number_serializer_mixin_serialize(self):
        data = MyDataNumberClass(str_field="Hola", date_field=date(2023, 1, 3))
        self.assertEqual(
            data.model_dump(), {"str_field": "Hola", "date_field": 20230103}
        )

    def test_date_number_serializer_mixin_deserialize(self):
        json_raw = '{"str_field": "hola", "date_field": 20190523}'
        my_dict = json.loads(json_raw)
        obj = MyDataNumberClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_number_serializer_mixin_deserialize_one_digit_month(self):
        json_raw = '{"str_field": "hola", "date_field": 20190503}'
        my_dict = json.loads(json_raw)
        obj = MyDataNumberClass(**my_dict)
        self.assertEqual(obj.date_field, date(2019, 5, 3))

    def test_date_number_serializer_mixin_deserialize_two_digit_year(self):
        json_raw = '{"str_field": "hola", "date_field": 1905003}'
        my_dict = json.loads(json_raw)
        with self.assertRaises(ValueError):
            MyDataNumberClass(**my_dict)

    def test_date_number_serializer_mixin_deserialize_value_error(self):
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)

        with self.assertRaises(ValueError):
            MyDataNumberClass(**my_dict)

    def test_date_number_serializer_mixin_deserialize_optional_empty(self):
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
