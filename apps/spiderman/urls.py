from django.urls import path, re_path
from .views import SpiderDataView, AddDataToMysql, SpiderDataListView, AnswerView

app_name = "spider"

urlpatterns = [
    path('spiderdata/', SpiderDataView.as_view(), name='spiderdata'),
    # path('add/', AddDataToMysql.as_view(), name='add'),
    path('spiderdata/data/', SpiderDataListView.as_view(), name='data'),
    path('answer', AnswerView.as_view(), name='answer'),
]
