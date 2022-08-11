from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from shop.models import Book, Author
from bookshelf.models import Bookshelf, ShelfBook


class TestBookshelfViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'account1'
        self.password = 'fw16FAW5e'
        self.user = User.objects.create_user(self.username, 'mail@gmail.com', self.password)
        self.user.save()

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

    def test_bookshelf_not_logged(self):
        response = self.client.get(reverse('bookshelf:bookshelf-list'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/bookshelf/')

    def test_bookshelf_no_book(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('bookshelf:bookshelf-list'))

        self.assertTrue(self.client.login(username=self.username, password=self.password))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

    def test_bookshelf(self):
        self.client.login(username=self.username, password=self.password)

        shelf = Bookshelf.objects.create(
            user=self.user
        )
        shelf.save()
        # test empty bookshelf
        response = self.client.get(reverse('bookshelf:bookshelf-list'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

        # test non-empty bookshelf
        shelf_book = ShelfBook.objects.create(
            user=self.user,
            mother_book=self.book
        )
        shelf_book.save()
        shelf.books.add(shelf_book)

        response = self.client.get(reverse('bookshelf:bookshelf-list'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['bookshelf'], Bookshelf.objects.get(user=self.user))

    def test_add_to_bookshelf(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('bookshelf:add-to-bookshelf', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

        # no bookshelf
        response = self.client.get(reverse('bookshelf:add-to-bookshelf', kwargs={'pk': self.book.pk}))
        self.assertEquals(response.status_code, 302)

        # bookshelf exist
        shelf = Bookshelf.objects.create(
            user=self.user
        )
        shelf.save()
        response = self.client.get(reverse('bookshelf:add-to-bookshelf', kwargs={'pk': self.book.pk}))
        self.assertEquals(response.status_code, 302)

    def test_remove_from_bookshelf(self):
        self.client.login(username=self.username, password=self.password)
        # book doesn't exist
        response = self.client.get(reverse('bookshelf:remove-from-bookshelf', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

        # book exist
        response = self.client.get(reverse('bookshelf:remove-from-bookshelf', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 302)
        # no bookshelf
        self.assertRedirects(response, reverse('shop:books-for-sale'))

        shelf = Bookshelf.objects.create(
            user=self.user
        )
        shelf.save()
        shelf_book = ShelfBook.objects.create(
            user=self.user,
            mother_book=self.book
        )
        shelf_book.save()
        shelf.books.add(shelf_book)
        response = self.client.get(reverse('bookshelf:remove-from-bookshelf', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 302)

    def test_book_not_rated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('bookshelf:rate-book', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

        response = self.client.get(reverse('bookshelf:rate-book', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 302)

    def test_book_rated(self):
        self.client.login(username=self.username, password=self.password)
        shelf = Bookshelf.objects.create(
            user=self.user
        )
        shelf.save()
        shelf_book = ShelfBook.objects.create(
            user=self.user,
            mother_book=self.book,
            user_rating=5
        )
        shelf_book.save()
        shelf.books.add(shelf_book)
        response = self.client.get(reverse('bookshelf:rate-book', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 302)