from datetime import timedelta

from django.test import TestCase
from ..models import Cart, CartItem, Product, Receipt
from products.models import Category, Brand, Discount, OffCode


class CartTest(TestCase):
    def setUp(self) -> None:
        self.cat = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test brand')
        self.dis1 = Discount.objects.create(type='percent', value=20, max_price=25000)
        self.dis2 = Discount.objects.create(type='amount', value=20000)
        self.prod1 = Product.objects.create(name='Test Product', category=self.cat, brand=self.brand, price=150000,
                                            discount=self.dis1)
        self.prod2 = Product.objects.create(name='Second Product', category=self.cat, brand=self.brand, price=25000,
                                            discount=self.dis2)
        self.off1 = OffCode.objects.create(type='percent', value=10, max_price=20000, unique_token='asdasd')
        self.off2 = OffCode.objects.create(type='amount', value=50000, min_buy_price=200000, title="Father's day",
                                           unique_token='aa')
        self.rec1 = Receipt.objects.create(unique_id=1123)
        self.cart1 = Cart.objects.create(off_code=self.off1, receipt=self.rec1)
        self.rec2 = Receipt.objects.create(unique_id=2341, delivery_time=timedelta(days=2))
        self.cart2 = Cart.objects.create(off_code=self.off2, receipt=self.rec2)
        self.item1 = CartItem.objects.create(product=self.prod1, count=3, cart=self.cart1)
        self.item2 = CartItem.objects.create(product=self.prod2, cart=self.cart1)
        self.item3 = CartItem.objects.create(product=self.prod1, cart=self.cart2)
        self.item4 = CartItem.objects.create(product=self.prod2, count=5, cart=self.cart2)

    def test_product_final_price(self):
        self.assertEqual(self.prod1.final_price, 125000)
        self.assertEqual(self.prod2.final_price, 5000)

    def test_CartItem_final_price(self):
        self.assertEqual(self.item1.final_price, 375000)
        self.assertEqual(self.item2.final_price, 5000)
        self.assertEqual(self.item3.final_price, 125000)
        self.assertEqual(self.item4.final_price, 25000)

    def test_receipt_total_price_without_offcode(self):
        self.assertEqual(self.rec1.total_price, 380000)
        self.assertEqual(self.rec2.total_price, 150000)

    def test_receipt_offcode(self):
        self.assertEqual(self.rec1.order_discount, 20000)
        self.assertEqual(self.rec2.order_discount, 0)
        self.assertEqual(self.rec1.cart.off_code.profit(self.rec2.total_price), 15000)
        self.assertEqual(self.rec2.cart.off_code.profit(self.rec1.total_price), 50000)

    def test_receipt_final_price_with_offcode(self):
        self.assertEqual(self.rec1.final_price, 360000)
        self.assertEqual(self.rec2.final_price, 150000)
