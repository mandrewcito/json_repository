import os
import json
import uuid
import threading

from ..errors.entity_not_found import EntityNotFound
from ..errors.more_than_one_result import MoreThanOneResult

class JsonContext(object):
    def __init__(
            self,
            enity_name,
            filepath="./",
            key_field="id",
            key_generate_func=lambda: str(uuid.uuid4())):
        self.file_path = os.path.join(filepath, "{0}s.json".format(enity_name))
        self.entity_name = enity_name
        self.session_values = []
        if not os.path.exists(self.file_path):
            self.commit()
        self.key_field = key_field
        self.key_generate_func = key_generate_func
        self.lock = threading.Lock()

    def open(self):
        self.lock.acquire()
        with open(self.file_path) as f:
            data = json.load(f)
            self.session_values = data["values"]

    def close(self):
        self.lock.release()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def exists(self, identifier):
        matches = list(filter(
            lambda x: x[self.key_field] == identifier,
            self.session_values))
        return len(matches) > 0

    def add(self, entity):
        if (self.key_field in entity and self.exists(entity[self.key_field])):
            self.delete(entity)
        else:
            entity[self.key_field] = self.key_generate_func()
        self.session_values.append(entity)
        return entity

    def delete(self, entity):
        self.session_values = list(filter(
            lambda x: x[self.key_field] != entity[self.key_field],
            self.session_values))

    def commit(self):
        with open(self.file_path, 'w+') as f:
            f.write(
                json.dumps(
                    {
                        "name": self.entity_name,
                        "values": self.session_values
                    }))

    def find(self, query_function=None):
        if query_function is None:
            return self.session_values
        return list(filter(query_function, self.session_values))

    def first( self, query_function):
        values = self.find(query_function=query_function)
        return  None if len(values) == 0 else values[0]

    def single( self, query_function):
        values = self.find(query_function=query_function)

        if len(values) is 0:
            raise EntityNotFound()

        if len(values) is not 1:
            raise MoreThanOneResult()

        return values[0]

    def get(self, identifier):
        if not self.exists(identifier):
            raise EntityNotFound("identifier not found")
        return self.find(lambda x: x[self.key_field] == identifier)[0]

    def get_all(self):
        return self.session_values
