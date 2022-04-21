from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from .models import Bookshelf, ShelfBook
from shop.models import Book


class BookshelfView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        try:
            bookshelf = Bookshelf.objects.get(user=self.request.user)
            if len(bookshelf.books.all()) < 1:
                messages.info(self.request, 'Your bookshelf is empty.')
                return redirect('shop:books-for-sale')
            context = {'bookshelf': bookshelf}
            return render(self.request, 'bookshelf_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Your bookshelf is empty.')
            return redirect('shop:books-for-sale')


@login_required
def add_to_bookshelf(request, pk):
    book = get_object_or_404(Book, pk=pk)
    shelf_book, created = ShelfBook.objects.get_or_create(
        user=request.user,
        mother_book=book
    )
    shelf_qs = Bookshelf.objects.filter(user=request.user)
    if shelf_qs.exists():
        shelf = shelf_qs[0]
        if shelf.books.filter(mother_book__pk=book.pk).exists():
            return redirect('bookshelf:bookshelf-list')
        else:
            shelf.books.add(shelf_book)
        return redirect('bookshelf:bookshelf-list')
    else:
        shelf = Bookshelf.objects.create(user=request.user)
        shelf.books.add(shelf_book)
        return redirect('bookshelf:bookshelf-list')


@login_required
def remove_from_bookshelf(request, pk):
    book = get_object_or_404(Book, pk=pk)
    shelf_qs = Bookshelf.objects.filter(user=request.user)
    if shelf_qs.exists():
        shelf = shelf_qs[0]
        if shelf.books.filter(mother_book__pk=book.pk).exists():
            shelf_book = ShelfBook.objects.filter(
                user=request.user,
                mother_book=book
            )[0]
            shelf.books.remove(shelf_book)
            return redirect('shop:books-for-sale')
    return redirect('shop:books-for-sale')


@login_required
def rated_by_user(request, pk):
    rating = int(request.GET.get('rating', -1))
    book = get_object_or_404(Book, pk=pk)
    rating_book, created = ShelfBook.objects.get_or_create(
        user=request.user,
        mother_book=book
    )
    if not rating_book.user_rating:
        book.ratings_sum += rating
        book.user_ratings_counter += 1
        book.save()
    else:
        previous_rating = rating_book.user_rating
        book.ratings_sum = book.ratings_sum - (previous_rating - rating)
        book.save()
    rating_book.user_rating = rating
    rating_book.save()
    return redirect('bookshelf:bookshelf-list')


