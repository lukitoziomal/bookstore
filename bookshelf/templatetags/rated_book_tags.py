from django import template
from bookshelf.models import Bookshelf

register = template.Library()


@register.filter
def is_book_rated(user, bk):
    shelf_qs = Bookshelf.objects.filter(user=user)
    if shelf_qs.exists():
        shelf = shelf_qs[0]
        if bk in shelf.rated_books.all():
            return True
