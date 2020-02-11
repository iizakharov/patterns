import jsonpickle
from models import Brand


class OrderSerializer:

    def serialize_brand(self, brand):
        return jsonpickle.dumps(brand)

    def deserialize_brand(self, json_brand):
        return jsonpickle.loads(json_brand)

    def serialize_items(self, items):
        return jsonpickle.dumps(items)

    def deserialize_items(self, json_items):
        return jsonpickle.loads(json_items)

    def dump_items(self, items, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            items_json = self.serialize_items(items)
            f.write(items_json)

    def load_items(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            items_json = f.read()
        items = self.deserialize_items(items_json)
        return items
