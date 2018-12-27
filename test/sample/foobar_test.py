import unittest
import os
from json_repository.repositories.base_json_repository import BaseJsonRepository
from json_repository.errors.entity_not_found import EntityNotFound

class FoobarRepository(BaseJsonRepository):
  def __init__(self):
    super(FoobarRepository, self).__init__("foo")


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        """
            ensure db is empty at the end.
        """
        with FoobarRepository() as repo:
            for entity in repo.get_all():
                repo.delete(entity)
            repo.context.commit()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        os.remove("foos.json")

    def test_insert(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar":" a bar value"
            })
            repo.context.commit()
        val2 = None
        with FoobarRepository() as repo:
            val2 = repo.get(value["id"])

        self.assertEqual(value, val2)

    def test_update(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            repo.context.commit()
        value["foo"] =" a new foo value"
        
        with FoobarRepository() as repo:
            repo.update(value)
            repo.context.commit()

        with FoobarRepository() as repo:
            val2 = repo.get(value["id"])

        self.assertEqual(value["foo"], val2["foo"])

    def test_delete(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            repo.context.commit()
        with FoobarRepository() as repo:
            repo.delete(value)
            repo.context.commit()

        with self.assertRaises(EntityNotFound):
            with FoobarRepository() as repo:
                repo.get(value["id"])

    def test_get_all(self):
        value = None
        value2 = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            value2 = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            repo.context.commit()
        values = [value, value2]
        with FoobarRepository() as repo:
            for value in repo.get_all():
                self.assertIn(value, values)

    def test_get(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            repo.context.commit()
        with FoobarRepository() as repo:
            self.assertEqual(value, repo.get(value["id"]))

    def test_find(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert({
                "foo": "a foo value",
                "bar": " a bar value"
            })
            repo.context.commit()
        with FoobarRepository() as repo:
            self.assertEqual(
                value,
                repo.find(lambda x: x["foo"] == value["foo"])[0])