from pytest import raises
from models import ItemFactory, Brand, CoffeeMachine
from dump import OrderSerializer


class TestOrderSerializer:

    def setup(self):
        item_factory = ItemFactory()
        self.brand = item_factory.create_brand('Lavazza')
        self.serializer = OrderSerializer()

    def test_serialize(self):
        result_json = self.serializer.serialize_brand(self.brand)
        brand = self.serializer.deserialize_brand(result_json)
        assert isinstance(brand, Brand)
        assert self.brand.name == brand.name
        item_factory = ItemFactory()
        self.coffee = item_factory.create_item('coffee', 'MilanoBar',
                                               12, brands=[self.brand])
        self.coffee_machine1 = CoffeeMachine('Saeco', 20, self.brand)
        self.coffee_machine2 = CoffeeMachine('Jura', 20, self.brand)
        self.coffee_machine = item_factory.create_item('repair',
                                                       name='Рермонт',
                                                       quantity=30,
                                                       price=100,
                                                       coffee_machines=[self.coffee_machine1, self.coffee_machine2])
        self.coffee_machine3 = CoffeeMachine('Gaggia', 20, self.brand)
        self.compilation = item_factory.create_item('compilation',
                                                    name='by me',
                                                    quantity=30,
                                                    theme='For Coffee')
        # files = [self.coffee_machine, self.coffee, self.coffee_machine3]
        items = [self.compilation]
        items_json = self.serializer.serialize_items(items)
        new_items = self.serializer.deserialize_items(items_json)
        assert isinstance(new_items, list)
        assert new_items[0].theme == 'For Coffee'

        self.serializer.dump_items(items, 'test_json')
        new_items = self.serializer.load_items('test_json')
        assert isinstance(new_items, list)
        assert new_items[0].theme == 'For Coffee'
