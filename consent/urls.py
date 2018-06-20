from django.conf.urls import url
from consent.views import ConsentView

urlpatterns = [
    url(r'^$', ConsentView.as_view()),
    url(r'^([0-9]+)/$', ConsentView.as_view()),
]
