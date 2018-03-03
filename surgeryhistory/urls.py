from django.conf.urls import url
from surgeryhistory.views import SurgeryHistoryView

urlpatterns = [
    url(r'^$', SurgeryHistoryView.as_view()),
    url(r'^([0-9]+)/$', SurgeryHistoryView.as_view()),
]
