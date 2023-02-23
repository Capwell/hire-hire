from django.db import models


class ContributorContact(models.Model):
    contributor = models.ForeignKey(
        'contributors.Contributor',
        verbose_name='член команды',
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    # по этому полю фронт сможет подставлять соответсвующие соцсети значки
    social_network = models.CharField(
        'название соцсети',
        max_length=150,
    )
    contact = models.URLField(
        'контакт',
        blank=True,
        null=True,
        help_text='Укажите ссылку (github, telegram, vk и другие)',
    )

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self):
        return f'{self.social_network}: {self.contact}'
