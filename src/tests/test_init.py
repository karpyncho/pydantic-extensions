import json

from datetime import date
from unittest import TestCase

from pydantic import BaseModel

from karpyncho.pydantic_extensions import DateSerializerMixin, DateDMYSerializerMixin


class MyDataClass(DateSerializerMixin, BaseModel):
    str_field: str
    date_field: date


class MyDataDMYClass(DateDMYSerializerMixin, BaseModel):
    str_field: str
    date_field: date


class DateSerializerMixinTest(TestCase):

    def test_date_serializer_mixin_serialize(self):
        data = MyDataClass(str_field="Hola", date_field=date(2023, 1, 13))
        self.assertEqual(data.model_dump(), {"str_field": "Hola", "date_field": "2023-01-13"})

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

class DateDMYSerializerMixinTest(TestCase):

    def test_date_dmy_serializer_mixin_serialize(self):
        data = MyDataDMYClass(str_field="Hola", date_field=date(2023, 1, 13))
        self.assertEqual(data.model_dump(), {"str_field": "Hola", "date_field": "13/01/2023"})

    def test_date_dmy_serializer_mixin_deserialize(self):
        json_raw = '{"str_field": "hola", "date_field": "23/05/2019"}'
        my_dict = json.loads(json_raw)
        obj = MyDataDMYClass(**my_dict)

        self.assertEqual(obj.date_field, date(2019, 5, 23))

    def test_date_dmy_serializer_mixin_deserialize_value_error(self):
        json_raw = '{"str_field": "hola", "date_field": "THIS IS NOT A DATE"}'
        my_dict = json.loads(json_raw)

        with self.assertRaises(ValueError):
            MyDataDMYClass(**my_dict)