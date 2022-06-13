from pysondb import db


class JSONRepository:
    def __init__(self, path) -> None:
        self._db = db.getDb(path)

    def get_by_id(self, id):
        return self._db.getById(id)

    def get_first_by_key_value(self, key, value):
        results = self._db.getByQuery({key: value})
        if len(results) > 0:
            return results[0]
        else:
            return None

    def get_by_key_value(self, key, value):
        return self._db.getByQuery({key: value})

    def get_all(self):
        return self._db.getAll()

    def update_by_id(self, id, dict):
        return self._db.updateById(id, dict)

    def update_all(self, query_dict, updated_dict):
        return self._db.updateByQuery(query_dict, updated_dict)

    def remove_by_id(self, id):
        return self._db.deleteById(id)
