from decimal import Decimal
import logging
import json
import uuid

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse, get_object_or_404

from yookassa import Configuration, Payment
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models import Currency
from yookassa.domain.models.receipt import Receipt, ReceiptItem
from yookassa.domain.notification import WebhookNotification
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

from orders.models import Order


logger = logging.getLogger('yandex_kassa')

CANCELLATION_REASONS = {
    '3d_secure_failed': 'не пройдена аутентификация по 3-D Secure',
    'call_issuer': 'оплата данным платежным средством отклонена по неизвестным причинам',
    'canceled_by_merchant': 'платеж отменен по API при оплате в две стадии',
    'card_expired': 'истек срок действия банковской карты',
    'country_forbidden': 'нельзя заплатить банковской картой, выпущенной в этой стране',
    'expired_on_capture': 'истек срок списания оплаты у двухстадийного платежа',
    'expired_on_confirmation': 'пользователь не подтвердил платеж за время, отведенное на оплату выбранным способом',
    'fraud_suspected': 'платеж заблокирован из-за подозрения в мошенничестве',
    'general_decline': 'причина не детализирована',
    'identification_required': 'превышены ограничения на платежи для кошелька в Яндекс.Деньгах',
    'insufficient_funds': 'не хватает денег для оплаты',
    'internal_timeout': 'технические неполадки на стороне ЮKassa',
    'invalid_card_number': 'неправильно указан номер карты',
    'invalid_csc': 'неправильно указан код CVV2 (CVC2, CID)',
    'issuer_unavailable': 'организация, выпустившая платежное средство, недоступна',
    'payment_method_limit_exceeded': 'исчерпан лимит платежей для данного платежного средства или вашего магазина',
    'payment_method_restricted': 'запрещены операции данным платежным средством',
    'permission_revoked': 'нельзя провести безакцептное списание, пользователь отозвал разрешение на автоплатежи',
    'unsupported_mobile_operator': 'нельзя заплатить с номера телефона этого мобильного оператора'
}

Configuration.account_id = settings.YK_SHOP_ID
Configuration.secret_key = settings.YK_SECRET_KEY


def payment_process(request, return_url=None):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        items = []
        for item in order.items.all():
            items.append({
                'description': str(item.product),
                'quantity': item.quantity,
                'amount': {
                    'value': str(item.get_cost()),
                    'currency': Currency.RUB
                },
                'vat_code': 1
            })

        if return_url is None:
            return_url = reverse('orders:order_detail', args=[order.id])

        payment_details = {
            'amount': {
                'value': order.get_total_cost(),
                'currency': Currency.RUB
            },
            'receipt': {
                'customer':{
                    'phone': order.phone,
                    'email': order.email,
                    'full_name': order.full_name
                },
                'tax_system_code': 1,
                'items': items
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': return_url
            },
            'metadata': {
                'order_id': order.id,
                'user': order.full_name
            },
            'capture': True,
            'description': str(order)

        }
        payment = Payment.create(payment_details, str(uuid.uuid4()))
        return HttpResponseRedirect(payment.confirmation.confirmation_url)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')