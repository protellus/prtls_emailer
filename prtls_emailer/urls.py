from django.urls import path
from prtls_emailer.views import SendEmailView

urlpatterns = [
    path("send/", SendEmailView.as_view(), name="send"),
]
