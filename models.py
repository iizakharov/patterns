from copy import deepcopy


class OrderItem:

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return '{}({})'.format(self.name, self.quantity)


class Brand:
    """
    Бренд/Производитель
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class Coffee(OrderItem):
    """
    Книга
    """

    def __init__(self, name, brands, quantity):
        self.brands = brands
        super().__init__(name, quantity)

    def __str__(self):
        str_item = super().__str__()
        brands = [str(a) for a in self.brands]
        return '{str_item} brands: {brands}'.format(str_item=str_item, brands=brands)


class CoffeeMachine(OrderItem):
    """
    Кофемашина
    """

    def __init__(self, name, quantity, brand):
        self.brand = brand
        super().__init__(name, quantity)

    def __str__(self):
        str_item = super().__str__()
        return '{str_item} brand: {brand}'.format(str_item=str_item, brand=self.brand)


class Repair(OrderItem):
    """
    Журнал
    """

    def __init__(self, name, quantity, price, coffee_machines=None):
        self.price = price
        self.coffee_machines = coffee_machines or []
        super().__init__(name, quantity)

    def __len__(self):
        return len(self.coffee_machines)


class LenAdapter:
    """
    Структурный паттерн ADAPTER. Приводит интерфейс 1-го объекта к другому
    Позволяет объект у которого нет длины привести к объекту с длиной
    """

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def __len__(self):
        # В данной реализации просто возвращаем 1
        return 1


class Compilation(OrderItem):
    """
    Содержит набор книг, журналов и статей
    """

    def __init__(self, name, quantity, theme):
        self.name = name
        self.quantity = quantity
        self.theme = theme
        self.items = []

    def __len__(self):
        """
        Структурный паттерн COMPOSITE. Используется для древовидных структур
        1. У узлов и листьев должен быть одинаковый интерфейс, в данном случае метод len
        2. Узлы в цикле вызывают методы у вложенных элементов, листья вызывают свои методы
        :return: Сколько разных материалов в коллекции
        """
        result_len = 0
        # У контейнера идем по вложенным элементам и для каждого считаем длину
        for item in self.items:
            # У объектов обязательно должна быть длина
            # Но у некоторых объектов их нету, поэтому используем паттерн ADAPTER
            if '__len__' not in dir(item):
                # Используем ADAPTER
                item = LenAdapter(item)
            # просто вызываем метод len
            result_len += len(item)
        return result_len


class ItemFactory:
    """
    Паттерн FATORY METHOD
    """
    types = {
        'coffee': Coffee,
        'coffee_machine': CoffeeMachine,
        'repair': Repair,
        'compilation': Compilation
    }

    def create_brand(self, name):
        # управляем созданием производителя
        return Brand(name)

    def create_item(self, item_type, name, quantity, **kwargs):
        """
        FACTORY METHOD, содает объект в зависимости от типа
        :param item_type:
        :param kwargs:
        :return: экземляр нужного нам класса в зависимости от типа
        """
        ItemCls = ItemFactory.types[item_type]
        item = ItemCls(name=name, quantity=quantity, **kwargs)
        return item


def copy_item(item):
    """
    Паттерн PROTOTYPE
    Создаем объект на основании уже готового
    :param item:
    :return:
    """
    return deepcopy(item)
