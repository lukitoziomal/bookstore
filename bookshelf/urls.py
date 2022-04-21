from django.urls import path
from . import views

app_name = 'bookshelf'
urlpatterns = [
    path('', views.BookshelfView.as_view(), name='bookshelf-list'),
    path('add-to-bookshelf/<int:pk>', views.add_to_bookshelf, name='add-to-bookshelf'),
    path('remove-from-bookshelf/<int:pk>', views.remove_from_bookshelf, name='remove-from-bookshelf'),
    path('rate-book/<int:pk>', views.rated_by_user, name='rate-book')
]