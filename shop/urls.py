from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.BookstoreView.as_view(), name='books-for-sale'),
    path('cart', views.CartView.as_view(), name='cart-view'),
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove-from-cart'),
    path('single-remove-from-cart/<int:pk>', views.single_remove_from_cart, name='single-remove-from-cart'),
    path('book/<int:pk>', views.BookView.as_view(), name='book-detail-view'),
    path('checkout', views.CheckoutView.as_view(), name='checkout-view')
]