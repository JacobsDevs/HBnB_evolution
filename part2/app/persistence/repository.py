from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    def get(self, obj_id):
        pass

    def get_all(self):
        pass

    def update(self, obj_id, data):
        pass

    def delete(self, obj_id):
        pass

    def get_by_attribute(self, attr_name, attr_value):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}
        print(f"Created new repository: {id(self)}")

    def add(self, obj):
        print(f"Adding object with ID {obj.id} to repository {id(self)}")
        self._storage[obj.id] = obj
        print(f"Repository now contains: {list(self._storage.keys())}")

    def get(self, obj_id):
        print(f"Getting object with ID {obj_id} from repository {id(self)}")
        print(f"Repository contains: {list(self._storage.keys())}")
        return self._storage.get(obj_id)

    def get_all(self):
        print(f"Getting all objects from repository {id(self)}")
        print(f"Repository contains: {list(self._storage.keys())}")
        return list(self._storage.values())

    def update(self, obj_id, data):
        print(f"Updating object with ID {obj_id} in repository {id(self)}")
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        print(f"Deleting object with ID {obj_id} from repository {id(self)}")
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        print(f"Looking for objects with {attr_name}={attr_value} in repository {id(self)}")
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
