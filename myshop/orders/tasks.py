from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from .models import Order
from myshop import celery_app


@celery_app.task
def order_created(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return f"Заказ с id {order_id} не существует."

    subject = f'Заказ № {order.id}'
    message = (f'Дорогой {order.first_name}, \n\n'
               f'ваш заказ успешно размещен.\n'
               f'Номер вашего заказа {order.id}')

    try:
        mail_sent = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.email]
        )
    except Exception as e:
        return f"Ошибка при отправке почты: {e}"

    return mail_sent
