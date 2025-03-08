from django.apps import AppConfig
import warnings
from django.conf import settings

class PrtlsEmailerConfig(AppConfig):
    name = "prtls_emailer"

    def ready(self):
        # This is a workaround to avoid circular imports
        # We need to import the signals after the app is ready
        if not hasattr(settings, "EMAIL_API_KEY") or not settings.EMAIL_API_KEY:
            warnings.warn(
                "EMAIL_API_KEY is not set. Please set it in your settings.py file."
            )
        
        if not hasattr(settings, "EMAIL_DEFAULT_SENDER") or not settings.EMAIL_DEFAULT_SENDER:
            warnings.warn(
                "EMAIL_DEFAULT_SENDER is not set. Please set it in your settings.py file."
            )

        if not hasattr(settings, "EMAIL_DEFAULT_FROM_NAME") or not settings.EMAIL_DEFAULT_FROM_NAME:
            warnings.warn(
                "EMAIL_DEFAULT_FROM_NAME is not set. Please set it in your settings.py file."
            )

        if not hasattr(settings, "EMAIL_DEFAULT_REPLY_TO") or not settings.EMAIL_DEFAULT_REPLY_TO:
            warnings.warn(
                "EMAIL_DEFAULT_REPLY_TO is not set. Please set it in your settings.py file."
            )
