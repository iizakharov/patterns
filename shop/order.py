from django.contrib.auth.decorators import login_required

from models import ItemFactory
from commands import CommandsInvoker


class Order:
    """
    Паттер FACADE. Обобщаем мелкие структуры в более крупные которые будет использовать клиент
    """

    def __init__(self, item_factory):
        self.item_factory = item_factory
        self.items = []
        self.command_invoker = CommandsInvoker()

    def commit(self):
        self.command_invoker.execute_commands()

    def rollback(self):
        self.command_invoker.rollback_commands()

    def create_brand(self, name):
        """
        Создаем автора с помощью библиотеки
        :param name: Имя автора
        :return: Автор
        """
        return self.item_factory.create_brand(name)

    def create_item(self, item_type, name, quantity, **kwargs):
        """
        Создаем нужный объект с помощью библиотеки
        :param item_type: тип объекта
        :param name: название
        :param quantity: количество страниц
        :param kwargs: другие параметры
        :return: нужный объект в зависимости от типа
        """
        return self.item_factory.create_item(item_type, name, quantity, **kwargs)

    def add_item(self, item, commit=True):
        command = lambda: self.items.append(item)
        self.command_invoker.store_command(command)
        if commit:
            self.commit()

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def remove_item(self, item, commit=True):
        command = lambda: self.items.remove(item)
        self.command_invoker.store_command(command)
        if commit:
            self.commit()

    def search(self, **kwargs):
        ITEM_TYPE = 'item_type'
        if ITEM_TYPE in kwargs:
            item_type = kwargs[ITEM_TYPE]
            ItemCls = ItemFactory.types[item_type]
        result = []
        for item in self:
            if isinstance(item, ItemCls):
                result.append(item)
        return result

    def __getitem__(self, item):
        return self.items[item]

    def dump_items(self, serializer, file_name):
        serializer.dump_items(self.items, file_name)

    def load_items(self, serializer, file_name):
        self.items = serializer.load_items(file_name)


class UserOrder(Order):
    """
    Паттерн PROXY как один из вариантов ограницения доступа к библиотеке
    """

    def __init__(self):
        order = Order(ItemFactory())
        self._order = order

    def create_brand(self, name):
        self._raise_permission_error()

    def dump_items(self, serializer, file_name):
        self._raise_permission_error()

    def load_items(self, serializer, file_name):
        self._raise_permission_error()

    def _raise_permission_error(self):
        raise PermissionError('Метод доступен только для сотридников')

    def create_item(self, item_type, name, quantity, **kwargs):
        self._raise_permission_error()

    def remove_item(self, item):
        self._raise_permission_error()

    def add_item(self, item):
        self._raise_permission_error()

    def __getitem__(self, item):
        return self._order.__getitem__(item)

    def __contains__(self, item):
        return self._order.__contains__(item)

    def __len__(self):
        return self._order.__len__()


class StaffOrder(Order):
    """
    Паттерн Proxy, доступны все методы
    Можно просто использовать Order
    Но тут видно, что эта библиотека для сотрудников и может добавиться какой то функционал
    """

    def __init__(self):
        super().__init__(ItemFactory())


class IsStaff:
    """
    Добавляем функцонал прав с помощью DECORATOR
    Написал для примера, т.к. пока нету групп и пользователей и скорее всего лучше подойдет PROXY
    """

    def __init__(self, user):
        self.user = user

    def __call__(self, method):
        """
        DECORATOR добавляем функционал проверки прав в любой метод
        :param method:
        :return:
        """
        def inner(*args, **kwargs):
            if self.user.is_staff():
                return method(*args, **kwargs)
            else:
                raise PermissionError('Доступ только для сотрудников')

        return inner
