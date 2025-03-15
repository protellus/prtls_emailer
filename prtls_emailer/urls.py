from django.urls import path
from prtls_emailer.views import SendEmailView
from prtls_emailer.views import tracking_pixel

urlpatterns = [
    path("send/", SendEmailView.as_view(), name="send"),
    path("track/pixel/<uuid:tracking_id>/", tracking_pixel, name="tracking_pixel"),
]
