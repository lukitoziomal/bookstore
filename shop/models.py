from django.db import models
from django.conf import settings


GENRES = (
    ('F', 'Fantasy'),
    ('D', 'Drama'),
    ('SF', 'Sci-Fi'),
    ('M', 'Mystery'),
    ('T', 'Thriller'),
    ('R', 'Romance'),
    ('P', 'Poem'),
    ('H', 'Horror')
)


class Book(models.Model):
    title = models.CharField(max_length=60)
    authors = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)
    genre = models.CharField(choices=GENRES, max_length=2)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    ratings_sum = models.IntegerField(default=0)
    user_ratings_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_book_rating(self):
        return round(self.ratings_sum / self.user_ratings_counter, 1)


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BookItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_subtotal_value(self):
        if self.item.discount_price:
            return round(self.quantity * self.item.discount_price, 2)
        return round(self.quantity * self.item.price, 2)

    def savings(self):
        return round(self.item.price - self.item.discount_price, 2)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(BookItem)
    completed = models.BooleanField(default=False)

    def get_cart_value(self):
        value = 0
        for cart_item in self.items.all():
            if cart_item.item.discount_price:
                value += cart_item.item.discount_price * cart_item.quantity
            else:
                value += cart_item.item.price * cart_item.quantity
        return round(value, 2)


class DeliveryDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    postal = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=15)
    paid = models.BooleanField(default=False)

