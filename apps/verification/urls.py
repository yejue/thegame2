from django.urls import path, re_path
from .views import image_code_view, CheckEmailView, SendMailView, check_nickname_view

app_name = "veri"

urlpatterns = [
    path("image_code/", image_code_view, name="image_code"),
    path("email/", CheckEmailView.as_view(), name="email"),
    path("sendmail/", SendMailView.as_view(), name="sendmail"),
    re_path("check=(?P<nickname>.{2,20})/", check_nickname_view, name="nickname"),
]
