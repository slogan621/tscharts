
from django.conf.urls import url
from surgerytype.views import SurgerytypeView

urlpatterns = [
    url(r'^$', SurgerytypeView.as_view()),
    url(r'^([0-9]+)/$', SurgerytypeView.as_view()),
]
