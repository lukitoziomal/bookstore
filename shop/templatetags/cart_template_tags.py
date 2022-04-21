from django import template
from shop.models import Cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(
            user=user,
            completed=False
        )
        if qs.exists():
            return qs[0].items.count()
    return 0