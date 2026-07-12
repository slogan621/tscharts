#(C) Copyright Syd Logan 2016-2026
#(C) Copyright Thousand Smiles Foundation 2016-2026
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

"""tscharts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.contrib import admin
from tscharts.views import *

admin.autodiscover()

app_name = 'tscharts'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^tscharts/v1/category/', include('category.urls')),
    re_path(r'^tscharts/v1/clinic/', include('clinic.urls')),
    re_path(r'^tscharts/v1/clinicstation/', include('clinicstation.urls')),
    re_path(r'^tscharts/v1/consent/', include('consent.urls')),
    re_path(r'^tscharts/v1/image/', include('image.urls')),
    re_path(r'^tscharts/v1/login/$', LoginView.as_view()),
    re_path(r'^tscharts/v1/logout/$', LogoutView.as_view()),
    re_path(r'^tscharts/v1/createuser/$', CreateUserView.as_view()),
    re_path(r'^tscharts/v1/createuser$', CreateUserView.as_view()),
    re_path(r'^tscharts/v1/updatepin/$', UpdatePINView.as_view()),
    re_path(r'^tscharts/v1/updatepassword/$', UpdatePasswordView.as_view()),
    re_path(r'^tscharts/v1/audiogram/', include('audiogram.urls')),
    re_path(r'^tscharts/v1/entexam/', include('entexam.urls')),
    re_path(r'^tscharts/v1/entsurgicalhistory/', include('entsurgicalhistory.urls')),
    re_path(r'^tscharts/v1/enthistory/', include('enthistory.urls')),
    re_path(r'^tscharts/v1/enthistoryextra/', include('enthistoryextra.urls')),
    re_path(r'^tscharts/v1/enttreatment/', include('enttreatment.urls')),
    re_path(r'^tscharts/v1/entdiagnosis/', include('entdiagnosis.urls')),
    re_path(r'^tscharts/v1/entdiagnosisextra/', include('entdiagnosisextra.urls')),
    re_path(r'^tscharts/v1/dentalcdt/', include('dentalcdt.urls')),
    re_path(r'^tscharts/v1/dentalstate/', include('dentalstate.urls')),
    re_path(r'^tscharts/v1/dentaltreatment/', include('dentaltreatment.urls')),
    re_path(r'^tscharts/v1/medicalhistory/', include('medicalhistory.urls')),
    re_path(r'^tscharts/v1/medications/', include('medications.urls')),
    re_path(r'^tscharts/v1/mexicanstates/', include('mexicanstates.urls')),
    re_path(r'^tscharts/v1/patient/', include('patient.urls')),
    re_path(r'^tscharts/v1/patient', include('patient.urls')),
    #re_path(r'^tscharts/v1/queue/', include('queue.urls')),
    #re_path(r'^tscharts/v1/queueentry/', include('queue.queueentryurls')),
    re_path(r'^tscharts/v1/register/', include('register.urls')),
    re_path(r'^tscharts/v1/returntoclinic/', include('returntoclinic.urls')),
    re_path(r'^tscharts/v1/returntoclinicstation/', include('returntoclinicstation.urls')),
    re_path(r'^tscharts/v1/routingslip/', include('routingslip.rsurls')),
    re_path(r'^tscharts/v1/routingslipcomment/', include('routingslip.rscommenturls')),
    re_path(r'^tscharts/v1/routingslipentry/', include('routingslip.rsentryurls')),
    re_path(r'^tscharts/v1/statechange/', include('statechange.urls')),
    re_path(r'^tscharts/v1/station/', include('station.urls')),
    re_path(r'^tscharts/v1/surgeryhistory/', include('surgeryhistory.urls')),
    re_path(r'^tscharts/v1/surgerytype/', include('surgerytype.urls')),
    re_path(r'^tscharts/v1/covidvac/', include('covidvac.urls')),
    re_path(r'^tscharts/v1/vaccine/', include('vaccine.urls')),
    re_path(r'^tscharts/v1/xray/', include('xray.urls')),
]

