# Generated by Django 4.2a1 on 2023-02-22 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duel',
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
                ('wrong_answers', models.IntegerField(default=0)),
                (
                    'owner',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='duel',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'дуэль',
                'verbose_name_plural': 'дуэли',
            },
        ),
        migrations.CreateModel(
            name='DuelQuestion',
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
                ('is_answered', models.BooleanField(verbose_name='дан ответ')),
                (
                    'duel',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='questions',
                        to='interview.duel',
                        verbose_name='дуэль',
                    ),
                ),
                (
                    'question',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='duel',
                        to='interview.question',
                        verbose_name='вопрос',
                    ),
                ),
            ],
            options={
                'verbose_name': 'вопрос в дуэли',
                'verbose_name_plural': 'вопросы в дуэли',
            },
        ),
        migrations.CreateModel(
            name='DuelPlayer',
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
                    'name',
                    models.CharField(
                        default='Игрок', max_length=100, verbose_name='имя игрока'
                    ),
                ),
                ('counter', models.IntegerField(default=0)),
                (
                    'duel',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='players',
                        to='interview.duel',
                    ),
                ),
            ],
            options={
                'verbose_name': 'участник дуэли',
                'verbose_name_plural': 'участники дуэли',
            },
        ),
    ]
