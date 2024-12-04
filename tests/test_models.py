import unittest

import sthali_db.models


class TestDefault(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = sthali_db.models.FieldSpecification.Default()  # type: ignore

        self.assertEqual(result.factory, None)
        self.assertEqual(result.value, None)

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        result = sthali_db.models.FieldSpecification.Default(func, 0)

        self.assertEqual(result.factory, func)
        self.assertEqual(result.value, 0)


class TestFieldSpecification(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = sthali_db.models.FieldSpecification("test_field_name", sthali_db.models.typing.Any)  # type: ignore

        self.assertEqual(result.name, "test_field_name")
        self.assertEqual(result.type, sthali_db.models.typing.Any)
        self.assertEqual(result.default, None)
        self.assertEqual(result.description, None)
        self.assertEqual(result.optional, None)
        self.assertEqual(result.title, None)

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        optional = True
        result = sthali_db.models.FieldSpecification(
            "test_field_name",
            str,
            {"factory": func, "value": 0},  # type: ignore
            "test_field_description",
            optional,
            "test_field_title",
        )

        self.assertEqual(result.name, "test_field_name")
        self.assertEqual(result.type, str)
        self.assertEqual(result.default.factory, func)  # type: ignore
        self.assertEqual(result.default.value, 0)  # type: ignore
        self.assertEqual(result.description, "test_field_description")
        self.assertEqual(result.optional, True)
        self.assertEqual(result.title, "test_field_title")

    async def test_type_annotated(self) -> None:
        field_specification = sthali_db.models.FieldSpecification("test_field_name", str)  # type: ignore

        result = field_specification.type_annotated

        self.assertEqual(result("str"), "str")
        self.assertEqual(result.__args__[0], str)
        self.assertEqual(result.__metadata__[0].title, "test_field_name")

    async def test_type_annotated_with_optional(self) -> None:
        field_specification = sthali_db.models.FieldSpecification("test_field_name", str, optional=True)  # type: ignore

        result = field_specification.type_annotated

        self.assertEqual(result.__args__[0], str | None)

    async def test_type_annotated_with_default_factory(self) -> None:
        def func() -> None:
            return

        field_specification = sthali_db.models.FieldSpecification(
            "test_field_name", str, {"factory": func, "value": 0}
        )  # type: ignore

        result = field_specification.type_annotated

        self.assertEqual(result.__metadata__[0].default_factory(), None)

    async def test_type_annotated_with_default_value(self) -> None:
        field_specification = sthali_db.models.FieldSpecification("test_field_name", str, {"value": 0})  # type: ignore

        result = field_specification.type_annotated

        self.assertEqual(result.__metadata__[0].default, 0)


class TestBase(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = sthali_db.models.Base()

        self.assertEqual(result.model_dump(), {})


class TestBaseWithId(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        _id = sthali_db.models.uuid.uuid4()
        result = sthali_db.models.BaseWithId(id=_id)

        self.assertEqual(result.model_dump(), {"id": _id})


class TestModels(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        _id = sthali_db.models.uuid.uuid4()

        result = sthali_db.models.Models("name", [])

        self.assertEqual(result.name, "name")
        self.assertEqual(result.create_model().model_dump(), {})
        self.assertEqual(result.response_model(**{"id": _id}).model_dump(), {"id": _id})
        self.assertEqual(result.update_model().model_dump(), {})

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        _id = sthali_db.models.uuid.uuid4()

        result = sthali_db.models.Models(
            name="name",
            fields=[
                sthali_db.models.FieldSpecification("test_field_name_1", str),  # type: ignore
                sthali_db.models.FieldSpecification("test_field_name_2", str, optional=True),  # type: ignore
                sthali_db.models.FieldSpecification("test_field_name_3", str, default={"factory": func}),  # type: ignore
                sthali_db.models.FieldSpecification("test_field_name_4", str, default={"value": "test_field_value_4"}),  # type: ignore
                sthali_db.models.FieldSpecification("test_field_name_5", str, default={"factory": func, "value": 1}),  # type: ignore
            ],
        )

        self.assertEqual(result.name, "name")
        self.assertEqual(
            result.create_model(**{"test_field_name_1": "test_field_value_1", "test_field_name_2": None}).model_dump(),
            {
                "test_field_name_1": "test_field_value_1",
                "test_field_name_2": None,
                "test_field_name_3": None,
                "test_field_name_4": "test_field_value_4",
                "test_field_name_5": None,
            },
        )
        self.assertEqual(
            result.response_model(
                **{"id": _id, "test_field_name_1": "test_field_value_1", "test_field_name_2": None}  # type: ignore
            ).model_dump(),
            {
                "id": _id,
                "test_field_name_1": "test_field_value_1",
                "test_field_name_2": None,
                "test_field_name_3": None,
                "test_field_name_4": "test_field_value_4",
                "test_field_name_5": None,
            },
        )
        self.assertEqual(
            result.update_model(**{"test_field_name_1": "test_field_value_1", "test_field_name_2": None}).model_dump(),
            {
                "test_field_name_1": "test_field_value_1",
                "test_field_name_2": None,
                "test_field_name_3": None,
                "test_field_name_4": "test_field_value_4",
                "test_field_name_5": None,
            },
        )
