from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from shop.models import Book, Author, BookItem, Cart


class TestCheckoutView(TestCase):

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

    def test_user_not_logged(self):
        response = self.client.get(reverse('shop:checkout-view'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/checkout')

    def test_cart_does_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('shop:checkout-view'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

    def test_checkout_cart(self):
        self.client.login(username=self.username, password=self.password)
        cart = Cart.objects.create(
            user=self.user
        )
        cart.save()

        # empty cart
        response = self.client.get(reverse('shop:checkout-view'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

        # non empty cart
        item = BookItem.objects.create(
            user=self.user,
            item=self.book
        )
        item.save()
        cart.items.add(item)

        response = self.client.get(reverse('shop:checkout-view'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['cart'], Cart.objects.get(user=self.user))

    def test_checkout_post_cart_does_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('shop:checkout-view'), data={})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

    def test_checkout_post(self):
        self.client.login(username=self.username, password=self.password)
        cart = Cart.objects.create(
            user=self.user
        )
        cart.save()
        item = BookItem.objects.create(
            user=self.user,
            item=self.book
        )
        item.save()
        cart.items.add(item)

        response = self.client.post(
            reverse('shop:checkout-view'),
            {
                'first_name': 'Q',
                'surname': 'W',
                'address1': 'adr1',
                'address2': 'adr2',
                'city': 'Z',
                'postal': '11111',
                'payment_method': 'P'
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:paypal-payment'))


class TestCart(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'account1'
        self.password = 'fw16FAW5e'
        self.user = User.objects.create_user(self.username, 'mail@gmail.com', self.password)
        self.user.save()

        self.client.login(username=self.username, password=self.password)

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

    def test_cart_view(self):
        # cart does not exist
        response = self.client.get(reverse('shop:cart-view'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

        # empty cart
        cart = Cart.objects.create(user=self.user)
        cart.save()

        response = self.client.get(reverse('shop:cart-view'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:books-for-sale'))

        # non empty cart
        cart.items.add(self.book_item)
        response = self.client.get(reverse('shop:cart-view'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['cart'], Cart.objects.get(user=self.user))

    def test_add_to_cart_create_cart(self):
        # item does not exist
        response = self.client.get(reverse('shop:add-to-cart', kwargs={'pk': 9}))
        self.assertEquals(response.status_code, 404)

        # item exists
        response = self.client.get(reverse('shop:add-to-cart', kwargs={'pk': self.book.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all()[0], BookItem.objects.get(pk=self.book_item.pk))

    def test_add_to_cart_cart_exists_no_item(self):
        cart = Cart.objects.create(user=self.user)
        cart.save()
        response = self.client.get(reverse('shop:add-to-cart', kwargs={'pk': self.book.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all()[0], BookItem.objects.get(pk=self.book_item.pk))
        self.assertRedirects(response, reverse('shop:cart-view'))

    def test_add_to_cart_cart_exists_and_item(self):
        cart = Cart.objects.create(user=self.user)
        cart.save()
        cart.items.add(self.book_item)
        self.assertEquals(Cart.objects.get(user=self.user).items.all()[0].quantity, 1)
        response = self.client.get(reverse('shop:add-to-cart', kwargs={'pk': self.book.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all()[0].quantity, 2)
        self.assertEquals(Cart.objects.get(user=self.user).items.all().count(), 1)
        self.assertRedirects(response, reverse('shop:cart-view'))

    def test_remove_from_cart_no_cart_and_item(self):
        # item does not exist
        response = self.client.get(reverse('shop:remove-from-cart', kwargs={'pk': 9}))
        self.assertEquals(response.status_code, 404)

        # cart does not exist
        response = self.client.get(reverse('shop:remove-from-cart', kwargs={'pk': self.book_item.pk}))
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart.save()
        cart.items.add(self.book_item)

        response = self.client.get(reverse('shop:remove-from-cart', kwargs={'pk': self.book_item.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all().count(), 0)
        self.assertFalse(BookItem.objects.filter(user=self.user).exists())

    def test_single_remove_from_cart_no_cart_and_item(self):
        # item does not exist
        response = self.client.get(reverse('shop:single-remove-from-cart', kwargs={'pk': 9}))
        self.assertEquals(response.status_code, 404)

        # cart does not exist
        response = self.client.get(reverse('shop:single-remove-from-cart', kwargs={'pk': self.book_item.pk}))
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_single_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart.save()
        cart.items.add(self.book_item)
        self.client.get(reverse('shop:add-to-cart', kwargs={'pk': self.book_item.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all()[0].quantity, 2)
        response = self.client.get(reverse('shop:single-remove-from-cart', kwargs={'pk': self.book_item.pk}))
        self.assertEquals(BookItem.objects.get(user=self.user).quantity, 1)

        # 1 quantity
        response = self.client.get(reverse('shop:single-remove-from-cart', kwargs={'pk': self.book_item.pk}))
        self.assertEquals(Cart.objects.get(user=self.user).items.all().count(), 0)
        self.assertFalse(BookItem.objects.filter(user=self.user).exists())


