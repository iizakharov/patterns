from pytest import raises
from models import OrderItem, Coffee, CoffeeMachine, Brand, ItemFactory, Repair, copy_item, Compilation


class TestOrderItem:

    def setup(self):
        self.li = OrderItem('TestName', 20)

    def test_init(self):
        assert self.li.name == 'TestName'
        assert self.li.quantity == 20

    def test_str(self):
        assert str(self.li) == 'TestName(20)'


class TestBrand:

    def setup(self):
        self.leo = Brand('Leo')
        self.max = Brand('Max')

    def test_init(self):
        assert self.leo.name == 'Leo'
        assert self.max.name == 'Max'

    def test_str(self):
        assert str(self.leo) == 'Leo'
        assert str(self.max) == 'Max'

    def test_eq(self):
        assert self.leo != self.max
        assert self.leo == self.leo
        # Авторы равны когда равны их имена
        assert self.leo == Brand('Leo')


class TestCoffee:

    def setup(self):
        self.leo = Brand('Leo')
        self.max = Brand('Max')
        self.brands = [self.leo, self.max]
        self.coffee = Coffee(name='Python', brands=self.brands, quantity=20)

    def test_init(self):
        assert self.coffee.name == 'Python'
        assert self.coffee.quantity == 20
        # У книги может быть много авторов
        assert len(self.coffee.brands) == 2
        self.coffee.brands.append(Brand('Kate'))
        assert len(self.coffee.brands) == 3
        assert self.leo in self.coffee.brands
        assert self.max in self.coffee.brands
        assert self.coffee.brands is self.brands

    def test_iherit(self):
        assert isinstance(self.coffee, OrderItem)

    def test_str(self):
        assert str(self.coffee) == "Python(20) brands: ['Leo', 'Max']"


class TestCoffeeMachine:

    def setup(self):
        self.brand = Brand('Leo')
        self.coffee_machine = CoffeeMachine('Python', 20, self.brand)

    def test_inherit(self):
        assert isinstance(self.coffee_machine, OrderItem)

    def test_init(self):
        assert self.coffee_machine.name == 'Python'
        assert self.coffee_machine.quantity == 20
        assert self.coffee_machine.brand is self.brand

    def test_str(self):
        assert str(self.coffee_machine) == 'Python(20) brand: Leo'


class TestRepair:

    def setup(self):
        self.empty_press = Repair('Аренда', 2, 100)
        self.coffee_machines = [CoffeeMachine('Python', 20, Brand('Leo')), CoffeeMachine('Java', 20, Brand('Max'))]
        self.press = Repair('IT', 30, 2, self.coffee_machines)

    def test_init(self):
        assert self.empty_press.name == 'Аренда'
        assert self.empty_press.quantity == 2
        assert self.empty_press.price == 100
        assert len(self.empty_press.coffee_machines) == 0
        assert len(self.press.coffee_machines) == 2

    def test_len(self):
        assert len(self.empty_press) == 0
        assert len(self.press) == 2


def test_create_item():
    # создаем книгу
    brand = Brand('Leo')
    item_factory = ItemFactory()
    coffee_item = item_factory.create_item('coffee', name='Python', quantity=20, brands=[brand])
    assert isinstance(coffee_item, OrderItem)
    assert isinstance(coffee_item, Coffee)
    assert coffee_item.name == 'Python'
    assert brand in coffee_item.brands
    # Что если создать книгу с неверными параметрами, что мы хотим получить
    with raises(Exception):
        # должно быть не автор а авторы
        item_factory.create_item('coffee', name='Python', quantity=20, brand=brand)
    # Какую ошибку мы ожидаем, key_error?
    # with raises(KeyError):
    #     create_item('coffee', name='Python', quantity=20, brand=brand)
    # Так не удобно распаковывать данные, возможно какую то свою специальную ошибку
    # Похоже TypeError подходит, он показывает какие параметры проущены
    with raises(TypeError):
        item_factory.create_item('coffee', name='Python', quantity=20, brand=brand)
    # создаем статью
    coffee_machine_item = item_factory.create_item('coffee_machine', name='Java', quantity=10, brand=Brand('Leo'))
    assert isinstance(coffee_machine_item, OrderItem)
    assert isinstance(coffee_machine_item, CoffeeMachine)
    # создаем журнал
    repair_item = item_factory.create_item('repair', name='c#', quantity=30, coffee_machines=[coffee_machine_item], price=100)
    assert isinstance(repair_item, OrderItem)
    assert isinstance(repair_item, Repair)
    # создаем что то чего нету
    with raises(KeyError):
        item_factory.create_item('what', name='what', quantity=1)

    # создаем сборку
    compilation_item = item_factory.create_item('compilation', name='by leo', quantity=30, theme='Program')
    assert isinstance(compilation_item, OrderItem)
    assert isinstance(compilation_item, Compilation)


def test_copy_item():
    item_factory = ItemFactory()
    coffee_item = item_factory.create_item('coffee', name='Python', quantity=20, brands=[])
    new_coffee = copy_item(coffee_item)
    # это разные объекты
    assert not coffee_item is new_coffee
    # но у них совпадают данные
    assert coffee_item.name == new_coffee.name


class TestCompilation:

    def setup(self):
        # общий автор
        self.brand = Brand('Leo')
        # 1 книга
        item_factory = ItemFactory()
        self.coffee = item_factory.create_item('coffee', 'TestCoffee', 12, brands=[self.brand])
        # 1 журнал в нем 2 статьи
        self.coffee_machine1 = CoffeeMachine('Python', 20, self.brand)
        self.coffee_machine2 = CoffeeMachine('Java', 20, self.brand)
        self.repair = item_factory.create_item('repair', name='Program', quantity=30,
                                                coffee_machines=[self.coffee_machine1, self.coffee_machine2], price=100)
        # Просто статья
        self.coffee_machine3 = CoffeeMachine('c#', 20, self.brand)
        # Создаем сборку
        self.compilation = item_factory.create_item('compilation', name='by leo', quantity=30, theme='Program')
        files = [self.repair, self.coffee, self.coffee_machine3]
        for f in files:
            self.compilation.items.append(f)
        # При желании можно создать сборку и полохить в неё другую сборку и так сколько угодно раз

    def test_len(self):
        # Можно проверить длину у любого объкта. Паттерн COMPOSITE
        assert len(self.compilation) == 4