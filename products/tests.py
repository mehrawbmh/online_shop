from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from online_shop.settings import TIME_ZONE
from .models import *


class ProductTest(TestCase):
    def setUp(self) -> None:
        TIME_ZONE = 'uct'
        self.cat1 = Category.objects.create(name='Base Category')
        self.cat2 = Category.objects.create(parent_id=self.cat1.id, name="Other Category")

        self.brand1 = Brand.objects.create(name='first brand')
        self.brand2 = Brand.objects.create(name='second brand', bio="Some explanation about it")

        self.dis1 = Discount.objects.create(type='percent', value=20)
        self.dis2 = Discount.objects.create(type='percent', value=30, max_price=15000)
        self.dis3 = Discount.objects.create(type='percent', value=5,
                                            expire_date=datetime(year=2022, month=2, day=14).date())
        self.dis4 = Discount.objects.create(type='amount', value=10000)
        self.dis5 = Discount.objects.create(type='amount', value=10000)
        self.dis6 = Discount.objects.create(type='amount', value=2000)
        self.dis7 = Discount.objects.create(type='amount', value=150000)
        self.dis8 = OffCode.objects.create(type='amount', value=5000, unique_token='aaa')

        self.item1 = Product.objects.create(name='product1', price=15000, brand=self.brand1, category=self.cat1,
                                            description="Some thing about this product")
        self.item2 = Product.objects.create(name='product2', price=25000, brand=self.brand2, category=self.cat1)
        self.item3 = Product.objects.create(name='product3', price=1000, brand=self.brand2, category=self.cat2)
        self.item4 = Product.objects.create(name='product4', price=5000, brand=self.brand1, category=self.cat2)
        self.item5 = Product.objects.create(name='product5', price=350000, brand=self.brand1, category=self.cat1)

    def test_category_parent(self):
        self.assertIsNone(self.cat1.parent)
        self.assertEqual(self.cat2.parent, self.cat1)

    def test_category_name(self):
        self.assertEqual(self.cat1.name, 'Base Category')
        self.assertNotEqual(self.cat2.name, 'OtherCategory')  # test white space in name
        self.assertNotEqual(self.cat2.name, 'other category')  # test uppercase letters

    def test_discount_expiration(self):
        self.dis3: Discount
        with self.assertRaises(ValidationError):
            self.dis3.is_valid()
        self.assertFalse(self.dis3.is_active)
        self.dis3.expire_date = datetime(2023, 7, 8).date()
        self.assertTrue(self.dis3.is_valid())

    def test_brand_and_base_model(self):
        self.assertEqual(self.brand1.name, 'first brand')
        self.brand1.name = 'sss'
        self.assertNotEqual(self.brand1.name, 'first brand')
        self.brand2.is_active = False
        self.assertFalse(self.brand2.is_active)
        self.assertTrue(self.brand1.is_active)
        # self.assertAlmostEqual(self.brand1.create_timestamp.hour, datetime.now().hour)
        print(self.brand1.create_timestamp)
        self.assertFalse(self.brand2.is_deleted)
        self.assertIsNone(self.brand1.bio)
        self.assertAlmostEqual(self.brand1.last_update.day, datetime.now().day)

    def test_discount_attributes(self):
        self.assertIsNone(self.dis1.max_price)
        self.assertIsNone(self.dis2.expire_date)
        self.assertEqual(self.dis3.value, 30)
        self.assertEqual(self.dis5.type, 'amount')

    def test_product_fields(self):
        self.assertEqual(self.item1.brand, self.brand1)
        self.assertEqual(self.item1.category, self.cat1)
        self.assertIsNone(self.item2.description)
        for item in Product.objects.all():
            item: Product
            self.assertGreaterEqual(item.final_price, 0)
            self.assertIsNone(item.discount)
            self.assertEqual(item.available_count, 10)

    def test_percent_discount(self):
        self.item1.discount = self.dis1
        self.item2.discount = self.dis1
        self.item3.discount = self.dis2
        self.item4.discount = self.dis3
        self.item5.discount = self.dis2
        self.assertEqual(self.item1.final_price, 12000)
        self.assertEqual(self.item2.final_price, 20000)
        self.assertEqual(self.item3.final_price, 700)
        self.assertEqual(self.item4.final_price, 4750)
        self.assertEqual(self.item5.final_price, 15000)  # test maximum price of discount!
        for prod in Product.objects.all():
            self.assertIs(type(prod.final_price), int)
            self.assertAlmostEqual(prod.last_update.minute, datetime.now().minute)

    def test_amount_discount(self):
        self.item1.discount = self.dis4
        self.item2.discount = self.dis5
        self.item3.discount = self.dis6
        self.item4.discount = self.dis7
        self.item5.discount = self.dis7

        def assign_test(item):
            item.discount.max_price = 5000

        with self.assertRaises(ValidationError):
            assign_test(self.item1)
        self.assertEqual(Discount.objects.get(id=4).product_set.first(), self.item1)
        self.assertIsNone(Product.objects.filter(discount__type='percent').all())
        self.assertEqual(self.item1.final_price, 5000)
        self.assertEqual(self.item2.final_price, 15000)
        self.assertEqual(self.item3.final_price, 0)
        self.assertEqual(self.item4.final_price, 0)
        self.assertIsNotNone(self.dis8.unique_token)

    def tearDown(self) -> None:
        TIME_ZONE = 'Asia/Tehran'
