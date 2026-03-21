"""Django Apps here"""

# pylint: disable=import-outside-toplevel, unused-import

from django.apps import AppConfig
class CaloriesConfig(AppConfig):
    """Calories Config Class."""

    name = "calories_app"

    def ready(self):
        import calories_app.signals
        