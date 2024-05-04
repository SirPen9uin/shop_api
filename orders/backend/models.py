from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название магазина')
    url = models.URLField(verbose_name='Ссылка на магазин', null=True, blank=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    shops = models.ManyToManyField(Shop)
    name = models.CharField(max_length=50, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    name = models.CharField(max_length=50, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(default=0, verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информация о продуктах'
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_info'),
        ]

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Информация о продукте')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметр')
    value = models.CharField(max_length=50, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]

    def __str__(self):
        return self.value


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, verbose_name='Статус')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Продукт')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанный продукт'
        verbose_name_plural = 'Заказанные продукты'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_item'),
        ]

    def __str__(self):
        return str(self.order)


class Contact(models.Model):
    type = models.CharField(max_length=15, verbose_name='Тип')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    value = models.CharField(max_length=50, verbose_name='Значение')
