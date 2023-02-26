# Generated by Django 4.2a1 on 2023-02-21 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('title', models.CharField(max_length=40, verbose_name='название')),
            ],
            options={
                'verbose_name': 'язык программирования',
                'verbose_name_plural': 'языки программирования',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'text',
                    models.CharField(max_length=256, verbose_name='текст вопроса'),
                ),
                (
                    'answer',
                    models.TextField(max_length=256, verbose_name='правильный ответ'),
                ),
                (
                    'language',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='questions',
                        to='interview.language',
                        verbose_name='вопрос',
                    ),
                ),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'questions',
                    models.ManyToManyField(
                        to='interview.question', verbose_name='набор вопросов'
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='interviews',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'интервью',
                'verbose_name_plural': 'интервью',
            },
        ),
    ]
