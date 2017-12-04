import datetime

from adminsortable.models import SortableMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from mptt.models import MPTTModel
import hashlib
import time

from application import settings
from burgershop.menuManager import CategoryManager
from burgershop.userManager import CustomUserManager


class City(models.Model):
    name = models.CharField(verbose_name='Название города', max_length=128)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class BurgerShop(models.Model):
    name = models.CharField(verbose_name='Название бургерной', max_length=256)
    city = models.ForeignKey(City, verbose_name='Город')

    class Meta:
        verbose_name = 'Бургерная'
        verbose_name_plural = 'Бургерные'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Логин (Имя пользователя)', max_length=255, unique=True, default=None,
                                error_messages={'unique': 'Пользователь с таким именем существует'})
    is_staff = models.BooleanField(verbose_name='Управляющий', default=False)

    is_dealer = models.BooleanField(verbose_name='Оператор', default=False)

    burgershop = models.ForeignKey(BurgerShop, verbose_name=u'Рестроан', default=None, null=True, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    object = CustomUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def authenticate_by_token(self):
        token = hashlib.sha256((self.username + str(self.pk) + settings.SECRET_KEY + str(time.time())).encode('utf-8')
        ).hexdigest()
        self.user_token.create(
            token=token,
            user=self,
        )
        return token


class AuthToken(models.Model):
    user = models.ForeignKey(User, related_name='user_token')
    token = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Токен авторизации'
        verbose_name_plural = 'Токены авторизации'


class MenuItem(models.Model):
    name = models.CharField(verbose_name='Название блюда', max_length=128)
    price = models.DecimalField(verbose_name='Стоитмость', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class MenuCategory(MPTTModel):
    name = models.CharField(verbose_name='Название категории', max_length=128)
    items = models.ManyToManyField(MenuItem, verbose_name='Блюдо', blank=True)
    parent = models.ForeignKey('self', verbose_name=u'Родительская категория',
                               related_name='child', default=None, blank=True, null=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = 'Катеогрия меню'
        verbose_name_plural = 'Категории меню'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_PAYED = 'p'
    STATUS_REJECTED = 'r'

    STATUS_CHOICES = (
        (STATUS_PAYED, 'Оплачен'),
        (STATUS_REJECTED, 'Отменен')
    )

    dealer = models.ForeignKey(User, verbose_name='Оператор')
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_PAYED, max_length=1)
    time = models.DateTimeField(verbose_name='Время создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return u'Заказ № {0}'.format(self.pk)

    def order_sum(self):
        counter = 0
        for item in self.order_items.all():
            counter += item.price
        return counter
    order_sum.short_description = 'Стоимость заказа'

    def order_burgershop(self):
        return self.dealer.burgershop
    order_burgershop.short_description = 'Бургерная'


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, verbose_name='Блюдо')
    price = models.DecimalField(verbose_name='Стоимость при покупке', max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, verbose_name=u'Заказ', related_name='order_items')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return self.item.name
