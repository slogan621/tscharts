
from django.conf.urls import url
from surgerytype.views import SurgeryTypeView

urlpatterns = [
    url(r'^$', SurgeryTypeView.as_view()),
    url(r'^([0-9]+)/$', SurgeryTypeView.as_view()),
]
