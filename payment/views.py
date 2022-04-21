from django.views.generic import FormView, View
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.shortcuts import render, redirect

from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Cart, DeliveryDetails


class PaypalFormView(FormView):
    template_name = 'paypal_payment.html'
    form_class = PayPalPaymentsForm

    def get_initial(self):
        try:
            cart = Cart.objects.get(
                user=self.request.user,
                completed=False
            )
            item_name = ''
            for product in cart.items.all():
                item_name += f'{product.quantity} x {product.item.title} '
        except ObjectDoesNotExist:
            messages.info(request, 'Your cart is empty.')
            return redirect('shop:books-for-sale')

        return {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart.get_cart_value(),
            'currency_code': 'USD',
            'item_name': item_name,
            'invoice': f'Invoice: {cart.pk}',
            'notify_url': self.request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': self.request.build_absolute_uri(reverse('payment:paypal-return')),
            'cancel_return': self.request.build_absolute_uri(reverse('payment:paypal-cancel')),
            'lc': 'EN'
        }


@csrf_exempt
def payment_done(request, **kwargs):
    context = {}
    cart_qs = Cart.objects.filter(
        user=request.user,
        completed=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        context['cart'] = cart
    order_qs = DeliveryDetails.objects.filter(
        user=request.user,
        paid=False
    )
    if order_qs.exists():
        order = order_qs[0]
        context['delivery'] = order
    messages.warning(request, 'Payment done. Your order is processing!')
    return render(request, 'payment_return.html', context)


@csrf_exempt
def payment_cancelled(request):
    try:
        orders_qs = DeliveryDetails.objects.filter(
            user=request.user,
            paid=False
        )
        order = orders_qs[0]
        order.delete()
    except ObjectDoesNotExist:
        return redirect('shop:books-for-sale')
    messages.error(request, 'Payment cancelled.')
    return redirect('shop:books-for-sale')

