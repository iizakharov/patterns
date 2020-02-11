from pytest import raises
from order import Order, ItemFactory, UserOrder, StaffOrder, IsStaff
from dump import OrderSerializer


class TestOrder:

    def setup(self):
        self.order = Order(ItemFactory())
        self.item = self.order.create_item('coffee', 'Sirocco', 12, brands=[self.order.create_brand('leo')])
        self.order.add_item(self.item)

    def test_len(self):
        assert len(self.order) == 1

    def test_contatins(self):
        assert self.item in self.order

    def test_remove_item(self):
        self.order.remove_item(self.item)
        assert len(self.order) == 0
        assert self.item not in self.order

    def test_search(self):
        coffees = self.order.search(item_type='coffee')
        assert len(coffees) == 1

    def test_iter(self):
        result = []
        for item in self.order:
            result.append(item)

        assert result[0] == self.item
        order_iterator = iter(self.order)
        first = next(order_iterator)
        assert first == self.item

    def test_serializer(self):
        serializer_visitor = OrderSerializer()
        self.order.dump_items(serializer_visitor, 'test_json')
        self.order.load_items(serializer_visitor, 'test_json')
        items = self.order.items
        assert isinstance(items, list)
        assert items[0].name == 'Sirocco'

    def test_commit_rollback(self):
        self.item = self.order.create_item('coffee', '1', 12, brands=[self.order.create_brand('leo')])
        self.order.add_item(self.item)
        assert len(self.order) == 2
        self.item = self.order.create_item('coffee', '2', 12, brands=[self.order.create_brand('leo')])
        self.order.add_item(self.item, commit=False)
        assert len(self.order) == 2
        self.item = self.order.create_item('coffee', '3', 12, brands=[self.order.create_brand('leo')])
        self.order.add_item(self.item, commit=False)
        assert len(self.order) == 2
        self.order.commit()
        assert len(self.order) == 4
        self.order.remove_item(self.item, commit=False)
        assert len(self.order) == 4
        self.order.rollback()
        assert len(self.order) == 4
        self.order.remove_item(self.item, commit=True)
        assert len(self.order) == 3


class TestUserOrder(TestOrder):

    def setup(self):
        self.order = UserOrder()
        self.item = self.order._order.create_item('coffee', 'Sirocco', 12,
                                                      brands=[self.order._order.create_brand('leo')])
        self.order._order.add_item(self.item)

    def test_remove_item(self):
        with raises(PermissionError):
            self.order.remove_item('some')

    def test_commit_rollback(self):
        with raises(PermissionError):
            self.order.add_item('some')

    def test_serializer(self):
        serializer_visitor = OrderSerializer()
        with raises(PermissionError):
            self.order.dump_items(serializer_visitor, 'test_json')
        with raises(PermissionError):
            self.order.load_items(serializer_visitor, 'test_json')


class TestStaffOrder(TestOrder):

    def setup(self):
        self.order = StaffOrder()
        self.item = self.order.create_item('coffee', 'Sirocco', 12, brands=[self.order.create_brand('leo')])
        self.order.add_item(self.item)


class TestIsStaff:
    """
    Пример теста декоратора с параметром
    """

    def setup(self):
        class User1:

            def is_staff(self):
                return True

        class User2:

            def is_staff(self):
                return False

        u1 = User1()
        u2 = User2()

        # создаем класс
        class Lib1:

            @IsStaff(u1)
            def method(self):
                return 123

        class Lib2:

            @IsStaff(u2)
            def method(self):
                return 123

        self.l1 = Lib1()
        self.l2 = Lib2()

    def test_call(self):
        assert self.l1.method() == 123
        with raises(PermissionError):
            self.l2.method()
