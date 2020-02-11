from pytest import raises
from models import OrderItem, Coffee, CoffeeMachine, Brand, ItemFactory,\
    Repair, copy_item, Compilation


class TestOrderItem:

    def setup(self):
        self.li = OrderItem('Mocca', 5)

    def test_init(self):
        assert self.li.name == 'Mocca'
        assert self.li.quantity == 5

    def test_str(self):
        assert str(self.li) == 'Mocca(5)'


class TestBrand:

    def setup(self):
        self.sirocco = Brand('Sirocco')
        self.lasemeuse = Brand('La Semeuse')

    def test_init(self):
        assert self.sirocco.name == 'Sirocco'
        assert self.lasemeuse.name == 'La Semeuse'

    def test_str(self):
        assert str(self.sirocco) == 'Sirocco'
        assert str(self.lasemeuse) == 'La Semeuse'

    def test_eq(self):
        assert self.sirocco != self.lasemeuse
        assert self.sirocco == self.sirocco
        # Авторы равны когда равны их имена
        assert self.sirocco == Brand('Sirocco')


class TestCoffee:

    def setup(self):
        self.sirocco = Brand('Sirocco')
        self.lasemeuse = Brand('La Semeuse')
        self.brands = [self.sirocco, self.lasemeuse]
        self.coffee = Coffee(name='Mocca', brands=self.brands, quantity=5)

    def test_init(self):
        assert self.coffee.name == 'Mocca'
        assert self.coffee.quantity == 5
        assert len(self.coffee.brands) == 2
        self.coffee.brands.append(Brand('Kate'))
        assert len(self.coffee.brands) == 3
        assert self.sirocco in self.coffee.brands
        assert self.lasemeuse in self.coffee.brands
        assert self.coffee.brands is self.brands

    def test_iherit(self):
        assert isinstance(self.coffee, OrderItem)

    def test_str(self):
        assert str(self.coffee) == "Mocca(5) brands: ['Sirocco', 'La Semeuse']"


class TestCoffeeMachine:

    def setup(self):
        self.brand = Brand('Saeco')
        self.coffee_machine = CoffeeMachine('Lirica', 20, self.brand)

    def test_inherit(self):
        assert isinstance(self.coffee_machine, OrderItem)

    def test_init(self):
        assert self.coffee_machine.name == 'Lirica'
        assert self.coffee_machine.quantity == 20
        assert self.coffee_machine.brand is self.brand

    def test_str(self):
        assert str(self.coffee_machine) == 'Lirica(20) brand: Saeco'


class TestRepair:

    def setup(self):
        self.service = Repair('Аренда', 2, 100)
        self.coffee_machines = [CoffeeMachine('Lirica', 20, Brand('Saeco')),
                                CoffeeMachine('Jura', 5, Brand('X9'))]
        self.catlog = Repair('Repair', 300, 2, self.coffee_machines)

    def test_init(self):
        assert self.service.name == 'Аренда'
        assert self.service.quantity == 2
        assert self.service.price == 100
        assert len(self.service.coffee_machines) == 0
        assert len(self.catlog.coffee_machines) == 2

    def test_len(self):
        assert len(self.service) == 0
        assert len(self.catlog) == 2


def test_create_item():
    brand = Brand('Sirocco')
    item_factory = ItemFactory()
    coffee_item = item_factory.create_item('coffee', name='Espresso',
                                           quantity=20, brands=[brand])
    assert isinstance(coffee_item, OrderItem)
    assert isinstance(coffee_item, Coffee)
    assert coffee_item.name == 'Espresso'
    assert brand in coffee_item.brands
    with raises(Exception):
        item_factory.create_item('coffee', name='Espresso',
                                 quantity=20, brand=brand)
    with raises(TypeError):
        item_factory.create_item('coffee', name='Espresso',
                                 quantity=20, brand=brand)
    coffee_machine_item = item_factory.create_item('coffee_machine',
                                                   name='Jura', quantity=10,
                                                   brand=Brand('Saeco'))
    assert isinstance(coffee_machine_item, OrderItem)
    assert isinstance(coffee_machine_item, CoffeeMachine)

    repair_item = item_factory.create_item('repair',
                                           name='Ремонт чего-то', quantity=30,
                                           coffee_machines=[coffee_machine_item], price=100)
    assert isinstance(repair_item, OrderItem)
    assert isinstance(repair_item, Repair)

    with raises(KeyError):
        item_factory.create_item('what', name='what', quantity=1)

    compilation_item = item_factory.create_item('compilation', name='by me',
                                                quantity=30, theme='Program')
    assert isinstance(compilation_item, OrderItem)
    assert isinstance(compilation_item, Compilation)


def test_copy_item():
    item_factory = ItemFactory()
    coffee_item = item_factory.create_item('coffee', name='Mocca',
                                           quantity=20, brands=[])
    new_coffee = copy_item(coffee_item)

    assert not coffee_item is new_coffee

    assert coffee_item.name == new_coffee.name


class TestCompilation:

    def setup(self):
        self.brand = Brand('Saeco')
        item_factory = ItemFactory()
        self.coffee = item_factory.create_item('coffee', 'Gold', 12,
                                               brands=[self.brand])

        self.coffee_machine1 = CoffeeMachine('Lirica', 20, self.brand)
        self.coffee_machine2 = CoffeeMachine('One Touch', 20, self.brand)
        self.repair = item_factory.create_item('repair', name='Program',
                                               quantity=30,
                                               coffee_machines=[self.coffee_machine1, self.coffee_machine2],
                                               price=100)

        self.coffee_machine3 = CoffeeMachine('Any', 20, self.brand)
        self.compilation = item_factory.create_item('compilation', name='by me', quantity=30, theme='Program')
        files = [self.repair, self.coffee, self.coffee_machine3]
        for f in files:
            self.compilation.items.append(f)

    def test_len(self):
        assert len(self.compilation) == 4
