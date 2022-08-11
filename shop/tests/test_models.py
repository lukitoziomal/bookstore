from django.test import TestCase, Client

from django.contrib.auth.models import User
from shop.models import Book, Author, BookItem, Cart


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'account1'
        self.password = 'fw16FAW5e'
        self.user = User.objects.create_user(self.username, 'mail@gmail.com', self.password)

        self.author = Author.objects.create(
            name='John Smith'
        )
        self.author.save()
        self.book = Book.objects.create(
            title='Test Title',
            authors=self.author,
            genre='F',
            description='qwer',
            price=9.99
        )
        self.book.save()

        self.book_item = BookItem.objects.create(
            user=self.user,
            item=self.book
        )
        self.book_item.save()

    def test_book_title(self):
        self.assertEquals(str(self.book), 'Test Title')

    def test_book_rating(self):
        self.book.ratings_sum = 40
        self.book.user_ratings_counter = 8
        self.assertEquals(self.book.get_book_rating(), 5.0)

    def test_book_item(self):
        self.assertEquals(str(self.book_item), 'Test Title')
        self.assertEquals(str(self.book_item), str(self.book))

        # test subtotal value
        self.assertEquals(self.book_item.get_subtotal_value(), self.book.price)

        self.book.discount_price = 7.99
        self.assertEquals(self.book_item.get_subtotal_value(), 7.99)

        self.book_item.quantity = 3
        self.assertEquals(self.book_item.get_subtotal_value(), 3*7.99)

        # test savings
        self.assertEquals(self.book_item.savings(), 9.99 - 7.99)

    def test_cart(self):
        cart = Cart.objects.create(
            user=self.user
        )
        cart.items.add(self.book_item)
        cart.save()

        self.assertEquals(cart.get_cart_value(), self.book.price)

        self.book.discount_price = 7.99
        self.book.save()
        self.assertEquals(cart.get_cart_value(), 7.99)