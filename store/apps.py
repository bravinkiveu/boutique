from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        from django.contrib.auth.models import update_last_login
        from django.contrib.auth.signals import user_logged_in
        try:
            user_logged_in.disconnect(update_last_login)
            print("Successfully disconnected update_last_login signal.")
        except Exception as e:
            print("Failed to disconnect update_last_login signal:", e)
