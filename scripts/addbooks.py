from django.core.exceptions import ObjectDoesNotExist
from shop.models import Book, Author

import random


BOOKS = {
    1: {'title': 'Parkers World',
        'author': 'Peter Parker',
        'description': 'Very cool book.',
        'genre': 'SF'},
    2: {'title': 'Story of John Smith',
        'author': 'John Smith',
        'description': 'Read about me.',
        'genre': 'D'},
    3: {'title': 'The Lord of the Rings',
        'author': 'J. R. R. Tolkien',
        'description': 'One ring to rule them all.',
        'genre': 'F'},
    4: {'title': 'Frankenstein',
        'author': 'Mary Shelley',
        'description': 'Very scary.',
        'genre': 'H'},
    5: {'title': 'And Then There Were None',
        'author': 'Agatha Christie',
        'description': 'The story follows ten people who are brought together, for various reasons.',
        'genre': 'M'},
    6: {'title': 'Gone Girl',
        'author': 'Gillian Flynn',
        'description': 'Story about Nick and Amy Dunnes strained marriage relationship.',
        'genre': 'T'}
}


def run():
    Book.objects.all().delete()
    Author.objects.all().delete()

    for key, book in BOOKS.items():
        print(key, book)
        author, created = Author.objects.get_or_create(
            name=book['author']
        )
        author.save()

        product = Book.objects.create(
            title=book['title'],
            authors=author,
            genre=book['genre'],
            description=book['description'],
            price=round(random.uniform(10, 25), 2)
        )
        if key % 2 == 0:
            product.discount_price = 7.99
        product.save()
