from django.core.mail import send_mail
from django.contrib.auth.models import User


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    if not is_admin:
        message = (f'Уважаемый {lead.name},\n\nПоддержка вашего продукта завершена. '
                   f'Если у вас возникнут вопросы, пожалуйста, свяжитесь с нами.\n\n'
                   f'С уважением,\nВаша команда поддержки')
    else:
        message = (f'Уважаемый администратор,\n\nПоддержка продукта пользователя {lead.name} завершена. '
                   f'Пожалуйста, примите соответствующие меры.\n\n'
                   f'С уважением,\nВаша команда поддержки')

    from_email = 'from@example.com'
    to_email = [user.email for user in User.objects.filter(is_staff=False)]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
