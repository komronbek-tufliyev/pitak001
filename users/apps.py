from django.apps import AppConfig



class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self) -> None:
        try:
            import users.signals
        except ImportError as e:
            print("Error importing users.signals", e)
            pass
