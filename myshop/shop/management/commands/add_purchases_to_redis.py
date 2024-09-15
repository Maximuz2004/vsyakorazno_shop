from django.core.management.base import BaseCommand, CommandError

from orders.models import Order
from shop.recommender import Recommender


class Command(BaseCommand):
    help = 'Добавляет информацию о купленных товарах в Redis для системы рекомендаций'

    def handle(self, *args, **kwargs):
        recommender = Recommender()
        orders = Order.objects.all()

        for order in orders:
            products = [item.product for item in order.items.all()]
            if products and len(products) > 1:
                recommender.products_bought(products=products)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Обработан заказ №{order.id} с товарами:'
                        f' {", ".join(str(product) for product in products)}'
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                'Завершено добавление информации о купленных товарах в Redis.'
            )
        )
