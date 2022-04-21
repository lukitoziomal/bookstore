from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver

from bookstore.settings import PAYPAL_RECEIVER_EMAIL
from shop.models import Cart, DeliveryDetails


@receiver(valid_ipn_received)
def is_valid_payment(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        if ipn.receiver_email != PAYPAL_RECEIVER_EMAIL:
            return False
        ipn_pk = int(ipn.invoice.split(' ')[1])
        cart = Cart.objects.get(pk=ipn_pk)
        ''' ipn.mc_gross returns type decimal.Decimal '''
        if float(ipn.mc_gross) == cart.get_cart_value() and ipn.mc_currency == 'USD':
            order = DeliveryDetails.objects.get(user=cart.user, paid=False)
            cart.completed = True
            cart.save()
            order.paid = True
            order.save()


@receiver(invalid_ipn_received)
def is_invalid_payment(sender, **kwargs):
    ipn_obj = sender
    return False

