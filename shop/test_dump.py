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
        # items
        # 1 книга
        item_factory = ItemFactory()
        self.coffee = item_factory.create_item('coffee', 'TestCoffee', 12, brands=[self.brand])
        # 1 журнал в нем 2 статьи
        self.coffee_machine1 = CoffeeMachine('Python', 20, self.brand)
        self.coffee_machine2 = CoffeeMachine('Java', 20, self.brand)
        self.journal = item_factory.create_item('repair', name='Рермонт', quantity=30, price=100,
                                                coffee_machines=[self.coffee_machine1, self.coffee_machine2])
        # Просто статья
        self.coffee_machine3 = CoffeeMachine('c#', 20, self.brand)
        # Создаем сборку
        self.compilation = item_factory.create_item('compilation', name='by leo', quantity=30, theme='Program')
        files = [self.journal, self.coffee, self.coffee_machine3]
        items = [self.compilation]
        items_json = self.serializer.serialize_items(items)
        new_items = self.serializer.deserialize_items(items_json)
        assert isinstance(new_items, list)
        assert new_items[0].theme == 'Program'
        # Запись в файл
        self.serializer.dump_items(items, 'test_json')
        new_items = self.serializer.load_items('test_json')
        assert isinstance(new_items, list)
        assert new_items[0].theme == 'Program'
