from django.urls import path, re_path
from .views import ThecodeView, CommentsView, GetURL, RegisterView

app_name = "thecode"

urlpatterns = [
    path("", ThecodeView.as_view(), name="thecode"),
    path("comments/", CommentsView.as_view(), name="comments"),
    re_path("url=(?P<tag>register)/", GetURL.as_view(), name="geturl"),
    path("098f6bcd4621d373cade4e832627b4f6/", RegisterView.as_view(), name="register"),
]
