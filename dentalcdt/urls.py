
from django.conf.urls import url
from dentalcdt.views import DentalCDTView

urlpatterns = [
    url(r'^$', DentalCDTView.as_view()),
    url(r'^([0-9]+)/$', DentalCDTView.as_view()),
]
