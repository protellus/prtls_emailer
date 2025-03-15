from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from prtls_emailer.models import EmailPixel

def tracking_pixel(request, tracking_id):
    """Returns a 1x1 transparent pixel and logs the email open event."""
    tracking = get_object_or_404(EmailPixel, tracking_id=tracking_id)
    tracking.mark_opened(request)

    # Transparent GIF (1x1)
    pixel_data = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B"
    return HttpResponse(pixel_data, content_type="image/gif")
