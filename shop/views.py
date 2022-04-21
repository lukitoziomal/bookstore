from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, ListView, DetailView

from .models import Book, BookItem, Cart, DeliveryDetails
from .forms import CheckoutForm


GENRES_LIST = ['Fantasy', 'Drama', 'Sci-Fi', 'Mystery', 'Thriller', 'Romance', 'Poem', 'Horror']
GENRES_DICT = {
    'Fantasy': 'F',
    'Drama': 'D',
    'Sci-Fi': 'SF',
    'Mystery': 'M',
    'Thriller': 'T',
    'Romance': 'R',
    'Poem': 'P',
    'Horror': 'H'
}


class BookstoreView(ListView):
    def get(self, *args, **kwargs):
        genre = self.request.GET.get('genre', -1)
        if genre in GENRES_LIST:
            books = Book.objects.filter(genre=GENRES_DICT[genre])
        else:
            books = Book.objects.all()
        context = {
            'all_books': books,
            'genres': GENRES_LIST
        }
        return render(self.request, 'bookstore.html', context)


class BookView(DetailView):
    model = Book
    template_name = 'book_view.html'
    context_object_name = 'book'


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(
                user=self.request.user,
                completed=False
            )
            if len(cart.items.all()) < 1:
                messages.info(self.request, 'Your cart is empty.')
                return redirect('shop:books-for-sale')
            form = CheckoutForm()
            context = {
                'cart': cart,
                'form': form
            }
            return render(self.request, 'checkout_view.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Your cart is empty.')
            return redirect('shop:books-for-sale')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            cart = Cart.objects.get(
                user=self.request.user,
                completed=False
            )
            if form.is_valid():
                payment_method = form.cleaned_data.get('payment_method')
                order_details = DeliveryDetails.objects.create(
                    user=self.request.user,
                    order=cart,
                    first_name=form.cleaned_data.get('first_name'),
                    surname=form.cleaned_data.get('surname'),
                    address1=form.cleaned_data.get('address1'),
                    address2=form.cleaned_data.get('address2'),
                    city=form.cleaned_data.get('city'),
                    postal=form.cleaned_data.get('postal'),
                    payment_method=payment_method
                )
                order_details.save()
                if payment_method == 'P':
                    return redirect('payment:paypal-payment')
        except ObjectDoesNotExist:
            messages.info(self.request, 'Your cart is empty.')
            return redirect('shop:books-for-sale')


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(
                user=self.request.user,
                completed=False
            )
            if len(cart.items.all()) < 1:
                messages.info(self.request, 'Your cart is empty.')
                return redirect('shop:books-for-sale')
            context = {'cart': cart}
            return render(self.request, 'cart_view.html', context)
        except ObjectDoesNotExist:
            return redirect('shop:books-for-sale')


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_item, created = BookItem.objects.get_or_create(
        user=request.user,
        item=item
    )
    cart_qs = Cart.objects.filter(
        user=request.user,
        completed=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('shop:cart-view')
        else:
            cart.items.add(order_item)
            return redirect('shop:cart-view')
    else:
        cart = Cart.objects.create(user=request.user)
        cart.items.add(order_item)
        return redirect('shop:cart-view')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    cart_qs = Cart.objects.filter(
        user=request.user,
        completed=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__pk=item.pk):
            order_item = BookItem.objects.filter(
                user=request.user,
                item=item
            )[0]
            cart.items.remove(order_item)
            order_item.delete()
            return redirect('shop:cart-view')
    return redirect('shop:cart-view')


@login_required
def single_remove_from_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    cart_qs = Cart.objects.filter(
        user=request.user,
        completed=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__pk=item.pk):
            order_item = BookItem.objects.filter(
                user=request.user,
                item=item
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                cart.items.remove(order_item)
                order_item.delete()
            return redirect('shop:cart-view')