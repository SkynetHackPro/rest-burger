# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 16:53
from __future__ import unicode_literals

import burgershop.userManager
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(default=None, error_messages={'unique': 'Пользователь с таким именем существует'}, max_length=255, unique=True, verbose_name='Логин (Имя пользователя)')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Имеет доступ в админку')),
                ('is_dealer', models.BooleanField(default=False, verbose_name='Оператор')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Пользователи',
                'verbose_name': 'Пользователь',
            },
            managers=[
                ('object', burgershop.userManager.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Токены авторизации',
                'verbose_name': 'Токен авторизации',
            },
        ),
        migrations.CreateModel(
            name='BurgerShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название бургерной')),
            ],
            options={
                'verbose_name_plural': 'Бургерные',
                'verbose_name': 'Бургерная',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название города')),
            ],
            options={
                'verbose_name_plural': 'Города',
                'verbose_name': 'Город',
            },
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название категории')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Категории меню',
                'verbose_name': 'Катеогрия меню',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название блюда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоитмость')),
            ],
            options={
                'verbose_name_plural': 'Блюда',
                'verbose_name': 'Блюдо',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'Оплачен'), ('r', 'Отменен')], default='p', max_length=1, verbose_name='Статус заказа')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Оператор')),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'Заказ',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоимость при покупке')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burgershop.MenuItem', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burgershop.Order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name_plural': 'Элементы заказа',
                'verbose_name': 'Элемент заказа',
            },
        ),
        migrations.AddField(
            model_name='menucategory',
            name='items',
            field=models.ManyToManyField(blank=True, to='burgershop.MenuItem', verbose_name='Блюдо'),
        ),
        migrations.AddField(
            model_name='menucategory',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='burgershop.MenuCategory', verbose_name='Родительская категория'),
        ),
        migrations.AddField(
            model_name='burgershop',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burgershop.City', verbose_name='Город'),
        ),
    ]
