from django.apps import AppConfig
#необходим для настройки текущего приложения

class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    # verbose_name - сработает в том случаи если в settings, мы в INSTALLED_APPS
    # передали women.apps.WomenConfig. Если только women, тогда бы не сработало
    verbose_name = 'Женщины мира'
