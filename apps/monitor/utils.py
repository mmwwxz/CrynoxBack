from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    from_email = 'crynox.devtes@gmail.com'
    five_days_later = timezone.now() + timedelta(seconds=59)

    if not is_admin:
        message = (f'Уважаемый {lead.name},\n\n'
                   f'Поддержка вашего продукта закончится через 5 дней.\n'
                   f'Если у вас возникнут вопросы или вы хотите продлить поддержку вашего продукта, пожалуйста, свяжитесь с нами.\n\n'
                   f'С уважением,\nВаша команда поддержки CRYNOX')
        to_email = [lead.email]
        if lead.updating == five_days_later.date():
            send_mail(subject, message, from_email, to_email, fail_silently=False)

    elif not is_admin:
        message = (f'Уважаемый {lead.name},\n\n'
                   'Поддержка вашего продукта завершена.\n'
                   'Если у вас возникнут вопросы или вы хотите продлить поддержку вашего продукта, пожалуйста, свяжитесь с нами.\n\n'
                   'С уважением,\nВаша команда поддержки CRYNOX')
        to_email = [lead.email]

    elif is_admin:
        message = (f'Уважаемый администратор,\n'
                   f'Поддержка продукта пользователя {lead.name} завершена.\n\n'
                   f'ФИО: {lead.name}\n'
                   f'Почта: {lead.email}\n'
                   f'Номер: {lead.phone}\n\n'
                   f'Дата окончания поддержки: {lead.updating}'
                   'Пожалуйста, примите соответствующие меры')
        to_email = [user.email for user in User.objects.filter(is_staff=True)]
        if lead.updating == five_days_later.date():
            send_mail(subject, message, from_email, to_email, fail_silently=False)

    else:
        message = (f'Уважаемый администратор,\n'
                   f'Поддержка продукта пользователя {lead.name} завершена.\n\n'
                   f'ФИО: {lead.name}\n'
                   f'Почта: {lead.email}\n'
                   f'Номер: {lead.phone}\n\n'
                   f'Дата окончания поддержки: {lead.updating}'
                   'Пожалуйста, примите соответствующие меры')
        to_email = [user.email for user in User.objects.filter(is_staff=True)]

    send_mail(subject, message, from_email, to_email, fail_silently=False)
