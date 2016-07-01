from django.conf.urls import url
from clinic.views import ClinicView

urlpatterns = [
    url(r'^$', ClinicView.as_view()),
    url(r'^/([0-9]+)/$', ClinicView.as_view()),
]

