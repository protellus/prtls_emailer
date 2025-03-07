from django.urls import path
from emailer.views import SendEmailView

urlpatterns = [
    path("send/", SendEmailView.as_view(), name="send"),
]
