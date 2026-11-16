from django.db import models
from main.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        PROCESSING = 'processing', 'В процессе'
        COMPLETED = 'completed', 'Завершен'

    class DeliveryMethod(models.TextChoices):
        PICKUP = 'pickup', 'Самовывоз'
        DELIVERY = 'delivery', 'Доставка'


    user_name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу',)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.NEW,verbose_name='Статус заказа',)
    email = models.EmailField(blank=True, verbose_name='Email',)
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethod.choices, default=DeliveryMethod.PICKUP, verbose_name='Способ доставки')

    def __str__(self):
        return f'Заказ №{self.pk} — {self.user_name}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} — {self.quantity} шт.'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    

