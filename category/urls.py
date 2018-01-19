
from django.conf.urls import url
from category.views import CategoryView

urlpatterns = [
    url(r'^$', CategoryView.as_view()),
    url(r'^([0-9]+)/$', CategoryView.as_view()),
]
