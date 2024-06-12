from django.apps import AppConfig


class TgBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tg_bot'

    # def ready(self):
    # import tg_bot.signals
