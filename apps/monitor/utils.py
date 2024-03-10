from django.core.mail import send_mail
from django.contrib.auth.models import User


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    from_email = 'crynox.devtes@gmail.com'

    if not is_admin:
        message = (f'Уважаемый {lead.name},\n\n'
                   'Поддержка вашего продукта завершена. '
                   'Если у вас возникнут вопросы, пожалуйста, свяжитесь с нами.\n\n'
                   'С уважением,\nВаша команда поддержки')
        to_email = [lead.email]
    else:
        message = (f'Уважаемый администратор,\n\n'
                   f'Поддержка продукта пользователя {lead.name} завершена. '
                   'Пожалуйста, примите соответствующие меры.\n\n'
                   'С уважением,\nВаша команда поддержки')
        to_email = [user.email for user in User.objects.filter(is_staff=True)]

    send_mail(subject, message, from_email, to_email, fail_silently=False)
