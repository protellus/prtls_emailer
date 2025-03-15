from django.db import models
import uuid
from django.utils.timezone import now

class EmailPixel(models.Model):
    email = models.EmailField()  # Recipient's email
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    opened = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def mark_opened(self, request):
        """Mark the email as opened."""
        if not self.opened:
            self.opened = True
            self.timestamp = now()
            self.ip_address = request.META.get("REMOTE_ADDR")
            self.user_agent = request.META.get("HTTP_USER_AGENT")
            self.save()
