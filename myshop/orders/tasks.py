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

# Запуск контейнера с брокером сообщений
# docker run -d -p 5672:5672 rabbitmq
# Запуск Celery:
#  celery -A myshop worker -l info -P eventlet
# Запуск flower:
# celery -A myshop flower
# todo посмотреть коммент: https://ru.stackoverflow.com/questions/1522508/djangocelery-%D0%BD%D0%B5-%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D0%B5%D1%82%D1%81%D1%8F-task
