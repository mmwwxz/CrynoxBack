from django.core.mail import send_mail
from django.urls import reverse
from .models import LeadSupport, User


def get_phone_link(phone_number):
    return f'<a href="tel:{phone_number}">{phone_number}</a>'


def get_site_link(domain_site):
    return f'<a href="{domain_site}">{domain_site}</a>' if domain_site else "неизвестен"


def get_lead_support_link(lead_support):
    lead_support_link = reverse(
        'admin:%s_%s_change' % (lead_support._meta.app_label, lead_support._meta.model_name),
        args=[lead_support.id]
    )
    return f'<a href="https://crynox.tech{lead_support_link}">Ссылка на запись пользователя</a>'


def send_support_completion_email(lead, is_admin=False):
    subject = 'Поддержка продукта завершена'
    from_email = 'crynox.devtes@gmail.com'
    info = LeadSupport.objects.first()

    message = ''
    to_email = ''

    if info:
        domain_site = info.domain_site
        lead_business = info.lead_business
    else:
        domain_site = None
        lead_business = None

    if not is_admin:
        name_or_business = lead.name or lead_business or " пользователь"
        message = (
            f'Здравствуйте уважаемый {name_or_business},<br><br>'
            f'Хотим вас оповестить об окончании тех.поддержки вашего продукта, '
            f'а именно {get_site_link(domain_site)}<br><br>'
            f'Если у вас есть вопросы насчет тех.поддержки или вы хотите ее продлить, '
            f'пожалуйста свяжитесь с нами!<br>Ответьте на данное сообщение, задайте вопрос или '
            f'звоните по номеру {get_phone_link(lead.phone)}.<br><br>'
            f'С уважением,<br>Ваша команда поддержки <a href="https://crynox.tech/">CRYNOX</a>'
        )
        to_email = [lead.email]
    elif is_admin:
        lead_number_link = get_phone_link(lead.phone)
        lead_support = LeadSupport.objects.filter(lead=lead).latest('updating')
        lead_support_link = get_lead_support_link(lead_support)
        message = (
            f'Уважаемый администратор,<br>'
            f'Поддержка продукта пользователя {lead.name} завершена.<br><br>'
            f'ФИО: {lead.name}<br>'
            f'Сайт: {get_site_link(domain_site)}<br>'
            f'Название бизнеса: {lead_business}<br>'
            f'Почта: {lead.email}<br>'
            f'Номер: {lead_number_link}<br><br>'
            f'Пожалуйста, примите соответствующие меры<br>'
            f'{lead_support_link}'
        )
        to_email = [user.email for user in User.objects.filter(is_staff=True)]

    send_mail(subject, message, from_email, to_email, fail_silently=False, html_message=message)
