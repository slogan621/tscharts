
from django.conf.urls import url
from covidvac.views import COVIDVacView

urlpatterns = [
    url(r'^$', COVIDVacView.as_view()),
    url(r'^([0-9]+)/$', COVIDVacView.as_view()),
]
