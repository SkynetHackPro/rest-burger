from adminsortable.models import SortableMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from burgershop.userManager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Логин (Имя пользователя)', max_length=255, unique=True, default=None,
                                error_messages={'unique': 'Пользователь с таким именем существует'})
    is_staff = models.BooleanField(verbose_name='Имеет доступ в админку', default=False)

    is_dealer = models.BooleanField(verbose_name='Оператор', default=False)

    USERNAME_FIELD = 'username'

    object = CustomUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class AuthToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Токен авторизации'
        verbose_name_plural = 'Токены авторизации'


class City(models.Model):
    name = models.CharField(verbose_name='Название города', max_length=128)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class BurgerShop(models.Model):
    name = models.CharField(verbose_name='Название бургерной', max_length=256)
    city = models.ForeignKey(City, verbose_name='Город')

    class Meta:
        verbose_name = 'Бургерная'
        verbose_name_plural = 'Бургерные'


class MenuItem(models.Model):
    name = models.CharField(verbose_name='Название блюда', max_length=128)
    price = models.DecimalField(verbose_name='Стоитмость', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class MenuCategory(SortableMixin):
    name = models.CharField(verbose_name='Название категории', max_length=128)
    items = models.ManyToManyField(MenuItem, verbose_name='Блюдо')

    class Meta:
        verbose_name = 'Катеогрия меню'
        verbose_name_plural = 'Категории меню'


class Order(models.Model):
    dealer = models.ForeignKey(User, verbose_name='Оператор')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, verbose_name='Блюдо')
    price = models.DecimalField(verbose_name='Стоимость при покупке', max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, verbose_name=u'Заказ')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
