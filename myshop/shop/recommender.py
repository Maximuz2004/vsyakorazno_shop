from django.conf import settings
import redis

from .models import Product

redis_conn = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender:
    def get_product_key(self, id: int):
        return f'product:{id}:purchased_with'

    def products_bought(self, products: list[Product]):
        product_ids = [product.id for product in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    redis_conn.zincrby(
                        self.get_product_key(product_id),
                        1,
                        with_id
                    )

    def suggest_products_for(self, products: list[Product], max_results=6):
        product_ids = [product.id for product in products]
        if len(products) == 1:
            suggestions = redis_conn.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True
            )[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            redis_conn.zunionstore(tmp_key, keys)
            redis_conn.zrem(tmp_key, *product_ids)
            suggestions = redis_conn.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            redis_conn.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            redis_conn.delete(self.get_product_key(id))
