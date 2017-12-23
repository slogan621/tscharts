
from django.conf.urls import url
from medications.views import MedicationsView

urlpatterns = [
    url(r'^$', MedicationsView.as_view()),
    url(r'^([0-9]+)/$', MedicationsView.as_view()),
]
