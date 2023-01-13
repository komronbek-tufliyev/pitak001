from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        try:
            import orders.signals
        except ImportError as e:
            print("Error", e)
            pass
        
        