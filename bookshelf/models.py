from django.db import models
from django.conf import settings
from shop.models import Book


class ShelfBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mother_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_rating = models.IntegerField(blank=True, null=True)

    def is_book_rated(self):
        shelf_qs = Bookshelf.objects.filter(user=self.user)
        if shelf_qs.exists():
            shelf = shelf_qs[0]
            if book in shelf.rated_books.all():
                return True
            return False


class Bookshelf(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField(ShelfBook)
