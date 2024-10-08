# ВсякоРазно🍭🍺🌺🚀

![Python3](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django4](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.x-darkgreen?logo=celery&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-orange?logo=rabbitmq&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6.x-red?logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.x-blue?logo=postgresql&logoColor=white)
![Yookassa](https://img.shields.io/badge/YooKassa-Payment-blueviolet?logo=yookassa&logoColor=white)

## О проекте

**"ВсякоРазно"** — это небольшой интернет-магазин, где можно найти разнообразные товары для любого случая. Проект представляет собой интернет-магазин с корзиной покупок, каталогом товаров, системой рекомендаций и возможностью оплаты.

## Функциональность

- **Каталог товаров** — пользователи могут просматривать товары по категориям.
- **Корзина покупок** — возможность добавления товаров в корзину с последующим оформлением заказа.
- **Рекомендации** — система рекомендаций товаров на основе истории покупок.
- **Система оплаты** — интеграция с платёжными системами для проведения онлайн-платежей.
- **Отправка уведомлений и счетов** - реализована возможность отправить уведомление на электронную почту клиента о заказе товара. А также счета в формате pdf с перечнем товаров, суммой заказа и статусом платежа.

## Технологии

Проект разработан с использованием следующих технологий:

- **Backend**: 
  - Python3, Django4
  - Celery и RabbitMQ для обработки асинхронных задач оправки уведомлений о заказе и счетов на оплату
  - Redis для обработки рекомендаций
  - PostgreSQL для базы данных
  - платежная система Yookassa

## Установка и развертывание

### Локальная установка

1. **Клонировать репозиторий:**

    ```bash
    git clone https://github.com/Maximuz2004/vsyakorazno_shop
    cd vsyakorazno_shop
    ```

2. **Создать виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux и macOS
    venv\Scripts\activate  # для Windows
    ```

3. **Установить зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настроить базу данных:**

    Для настройки базы данных, отредактируйте файл `.env`, добавив параметры вашей базы данных:
    ```dotenv
    SECRET_KEY=Ваш_секретный_ключ
    
    ALLOWED_HOSTS=доступные_хосты
    
    # Настройки БД
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=имя_вашей_БД
    DB_USER=пользователь
    POSTGRES_PASSWORD=пароль
    DB_HOST=хост_БД
    DB_PORT=порт_БД
    
    # Настройки почты
    EMAIL_HOST=сервер_почты
    EMAIL_HOST_USER=пользователь_почты
    EMAIL_HOST_PASSWORD=пароль_от_почты
    EMAIL_PORT=порт
    #EMAIL_USE_TLS=True
    EMAIL_USE_SSL=True
    
    # Yookassa данные для аутентификации
    YK_SHOP_ID=id_магазина
    YK_SECRET_KEY=секретный_ключ_магазина
    
    # Настройка Redis
    REDIS_HOST=хост_сервера_Редис
    REDIS_PORT=порт
    REDIS_DB=Номер_БД
    
    ```

    Выполните миграции:

    ```bash
    python manage.py migrate
    ```

5. **Запуск серверов:**
    - запустить Celery (для Windows [подробности](https://ru.stackoverflow.com/questions/1522508/djangocelery-%D0%BD%D0%B5-%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D0%B5%D1%82%D1%81%D1%8F-task))
    ```bash
    celery -A myshop worker -l info -P eventlet
    ```

    - запустить контейнер с брокером сообщений
    ```bash
    docker run -d -p 5672:5672 rabbitmq
    ```

    - запустить сервер разработки
    ```bash
    python manage.py runserver
    ```
   - запустить при необходимости flower для Celery
   ```bash
   celery -A myshop flower
   ```
    - установить, настроить и запустить ngrok для проверки работы вебхуков процесса оплаты


6. **Запуск Redis**

    Для работы с рекомендациями, его нужно через Docker:

    ```bash
    docker run -it --rm --name redis -p 6379:6379 redis
    ```


**Автор**: [Титов Максим](https://github.com/Maximuz2004)

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](./LICENSE).