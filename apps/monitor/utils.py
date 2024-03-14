from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from apps.monitor.models import LeadSupport


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    from_email = 'crynox.devtes@gmail.com'
    info = LeadSupport.objects.all()
    phone_number = "+996706661133"
    link_crynox = "https://crynox.tech/"
    name_or_business = lead.name if lead.name else info.lead_business

    if not is_admin:
        message = (f'Здравствуйте уважаемый {name_or_business},\n\n'
                    f'Хотим вас оповестить об окончании тех.поддержки вашего продукта, а именно <a href="{info.domain_site}">{info.domain_site}</a>\n\n'
                    f'Если у вас есть вопросы насчет тех.поддержки или вы хотите ее продлить, пожалуйста свяжитесь с нами! Ответьте на данное сообщение, задайте вопрос или <a href="tel:{phone_number}">позвоните по номеру {phone_number}</a>.\n\n'
                    f'С уважением,\nВаша команда поддержки <a href="{link_crynox}">CRYNOX</a>')
        to_email = [lead.email]
    elif is_admin:
        message = (f'Уважаемый администратор,\n'
                   f'Поддержка продукта пользователя {lead.name} завершена.\n\n'
                   f'ФИО: {lead.name}\n'
                   f'Сайт: {info.domain_site}\n'
                   f'Название бизнеса: {info.lead_business}\n'
                   f'Почта: {lead.email}\n'
                   f'Номер: {lead.phone}\n\n'
                   'Пожалуйста, примите соответствующие меры')
        to_email = [user.email for user in User.objects.filter(is_staff=True)]

    send_mail(subject, message, from_email, to_email, fail_silently=False)

# def send_support_completion_email(lead, is_admin=False):
#     subject = 'Поддержка продукта завершена'
#     from_email = 'crynox.devtes@gmail.com'
#     five_minutes_later = timezone.now() + timedelta(minutes=5)
#
#     lead_support = LeadSupport.objects.filter(lead=lead).latest('updating')
#
#     if not is_admin:
#         if lead_support.updating <= five_minutes_later and lead_support.updating > timezone.now():
#             message = (
#                 f'Уважаемый {lead.name},\n\n'
#                 f'Поддержка вашего продукта закончится через 5 дней.\n'
#                 f'Дата окончания поддержки: {lead_support.updating}\n'
#                 f'Если у вас возникнут вопросы или вы хотите продлить поддержку вашего продукта, пожалуйста, свяжитесь с нами.\n\n'
#                 f'С уважением,\nВаша команда поддержки CRYNOX'
#             )
#             to_email = [lead.email]
#             send_mail(subject, message, from_email, to_email, fail_silently=False)
#         elif lead_support.updating < timezone.now():
#             message = (
#                 f'Уважаемый {lead.name},\n\n'
#                 'Поддержка вашего продукта завершена.\n'
#                 'Если у вас возникнут вопросы или вы хотите продлить поддержку вашего продукта, пожалуйста, свяжитесь с нами.\n\n'
#                 'С уважением,\nВаша команда поддержки CRYNOX'
#             )
#             to_email = [lead.email]
#             send_mail(subject, message, from_email, to_email, fail_silently=False)
#
#     elif is_admin:
#         if lead_support.updating <= five_minutes_later and lead_support.updating > timezone.now():
#             message = (
#                 f'Уважаемый администратор,\n'
#                 f'Поддержка продукта пользователя {lead.name} закончится через 5 дней.\n\n'
#                 f'ФИО: {lead.name}\n'
#                 f'Почта: {lead.email}\n'
#                 f'Номер: {lead.phone}\n\n'
#                 f'Дата окончания поддержки: {lead_support.updating}'
#                 'Пожалуйста, примите соответствующие меры'
#             )
#             to_email = [user.email for user in User.objects.filter(is_staff=True)]
#             send_mail(subject, message, from_email, to_email, fail_silently=False)
#
#         elif lead_support.updating < timezone.now():
#             message = (
#                 f'Уважаемый администратор,\n'
#                 f'Поддержка продукта пользователя {lead.name} завершена.\n\n'
#                 f'ФИО: {lead.name}\n'
#                 f'Почта: {lead.email}\n'
#                 f'Номер: {lead.phone}\n\n'
#                 f'Дата окончания поддержки: {lead_support.updating}'
#                 'Пожалуйста, примите соответствующие меры'
#             )
#             to_email = [user.email for user in User.objects.filter(is_staff=True)]
#             send_mail(subject, message, from_email, to_email, fail_silently=False)
