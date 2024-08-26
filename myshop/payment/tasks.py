from io import BytesIO

from celery import shared_task
import weasyprint

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def payment_completed_send_email(order_id):
    order = get_object_or_404(Order, id=order_id)
    subject = f'Магазин ВсякоРазно Счет-фактура №{order.id}'
    message = (f'Здравствуйте, \nВо вложении вы найдете счет-фактуру по вашему'
               f' заказу №{order.id}.\n\nВаш магазин ВсякоРазно')
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.email]
    )
    print(order)
    html = render_to_string(
        'orders/order/pdf.html',
        {'order': order}
    )
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(
        f'order_{order.id}.pdf',
        out.getvalue(),
        'aplication/pdf'
    )
    try:
        email.send()
    except Exception as e:
        return f"Ошибка при отправке почты: {e}"