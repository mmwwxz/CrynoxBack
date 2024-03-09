from django.apps import AppConfig


class LandingPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.monitor'
    verbose_name = 'Мониторинг'

    def ready(self) -> None:
        import apps.monitor.signals
