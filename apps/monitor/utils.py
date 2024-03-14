from django.core.mail import send_mail
from django.contrib.auth.models import User
from apps.monitor.models import LeadSupport


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    from_email = 'crynox.devtes@gmail.com'
    info = LeadSupport.objects.first()

    if info:
        domain_site = info.domain_site
        lead_business = info.lead_business
    else:
        domain_site = None
        lead_business = None

    number = '+996706661133'
    phone_number = f'<a href="tel:{number}">позвоните по номеру {number}</a>'
    link_crynox = "<a href='https://crynox.tech/'>CRYNOX</a>"

    message = ""
    to_email = []

    if domain_site:
        site_link = f'<a href="{domain_site}">{domain_site}</a>'
    else:
        site_link = "неизвестен"

    if lead.name:
        name_or_business = lead.name
    elif lead_business:
        name_or_business = lead_business
    else:
        name_or_business = "Уважаемый пользователь"

    if not is_admin:
        message = (
            f'Здравствуйте уважаемый {name_or_business},\n\n'
            f'Хотим вас оповестить об окончании тех.поддержки вашего продукта, '
            f'а именно {site_link}\n\n'
            f'Если у вас есть вопросы насчет тех.поддержки или вы хотите ее продлить, '
            f'пожалуйста свяжитесь с нами! Ответьте на данное сообщение, задайте вопрос или '
            f'звоните по номеру {phone_number}.\n\n'
            f'С уважением,\nВаша команда поддержки {link_crynox}'
        )
        to_email = [lead.email]
    elif is_admin:
        message = (
            f'Уважаемый администратор,\n'
            f'Поддержка продукта пользователя {lead.name} завершена.\n\n'
            f'ФИО: {lead.name}\n'
            f'Сайт: {site_link}\n'
            f'Название бизнеса: {info.lead_business}\n'
            f'Почта: {lead.email}\n'
            f'Номер: {lead.phone}\n\n'
            f'Пожалуйста, примите соответствующие меры'
        )
        to_email = [user.email for user in User.objects.filter(is_staff=True)]
    send_mail(subject, message, from_email, to_email, fail_silently=False, html_message=message)
