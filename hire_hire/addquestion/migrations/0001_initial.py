# Generated by Django 4.2a1 on 2023-03-06 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('interview', '0007_alter_interview_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddQuestion',
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
                ('text', models.TextField(verbose_name='текст вопроса')),
                ('answer', models.TextField(verbose_name='правильный ответ')),
                (
                    'author',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='addquestions',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='автор',
                    ),
                ),
                (
                    'language',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='addquestions',
                        to='interview.language',
                        verbose_name='язык',
                    ),
                ),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
                'abstract': False,
            },
        ),
    ]
