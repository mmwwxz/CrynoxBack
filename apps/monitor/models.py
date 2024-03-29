from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.files import ImageField


class LeadStatusChoices(models.TextChoices):
    NEW_LEAD = 'NL', _('Новый запрос')
    FIRST_CONTACT = 'FC', _('Первый контакт')
    NEGOTIATIONS = 'NG', _('В процессе переговоров')
    CONTRACT_SIGNED = 'CS', _('Контракт заключен')


class UserForm(models.Model):
    name = models.CharField(verbose_name=_('ФИО'), max_length=255)
    phone = models.CharField(verbose_name=_("Номер телефона"), max_length=25)
    email = models.EmailField(_('Электронная почта'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=2,
        choices=LeadStatusChoices.choices,
        default=LeadStatusChoices.NEW_LEAD,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")


class LeadStatus(models.Model):
    contract = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Контракт"))
    design = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Дизайн"))
    back = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Бэкенд"))
    front = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Фронтенд"))
    testing = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Тестирование"))
    mvp = models.BooleanField(default=False, verbose_name=_("MVP"))

    lead = models.ForeignKey(UserForm, on_delete=models.CASCADE, verbose_name=_("Лид"))

    def __str__(self):
        return f"{self.lead.name} - Статусы"

    class Meta:
        verbose_name = _("Статус разработки")
        verbose_name_plural = _("Статусы разработок")


class LeadSupport(models.Model):
    lead_business = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Название компании"))
    domain_site = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Домен сайта"))
    testing = models.DateTimeField(verbose_name=_("Начало"))
    updating = models.DateTimeField(verbose_name=_("Окончание"))

    lead = models.ForeignKey(UserForm, on_delete=models.CASCADE, verbose_name=_("Лид"))

    def __str__(self):
        return f"{self.testing} - {self.updating}"

    class Meta:
        verbose_name = _("Поддержка продукта")
        verbose_name_plural = _("Поддержка продуктов")


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Тип содержимого",
                                     limit_choices_to={'model__in': ['leadstatus', 'leadsupport', 'userform', 'comment', 'user']})

    object_id = models.PositiveIntegerField(verbose_name="ID объекта")
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Комментарий от {self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


class Portfolio(models.Model):
    language = models.CharField(max_length=255, verbose_name="Язык")
    project_name = models.CharField(max_length=255, verbose_name="Название проекта")
    framework = models.CharField(max_length=255, verbose_name="Фреймворк")
    img = ImageField(upload_to='portfolio_img/', verbose_name="Картинка")
    url = models.URLField(max_length=300, verbose_name="Ссылка на проект")

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = _("Наше Портфорило")
        verbose_name_plural = _("Наши Портфорило")


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name="Язык на кнопке")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Язык на кнопке")
        verbose_name_plural = _("Языки на кнопке")
