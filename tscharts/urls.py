#(C) Copyright Syd Logan 2016-2023
#(C) Copyright Thousand Smiles Foundation 2016-2023
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
from django.conf.urls import url, include
from django.contrib import admin
from tscharts.views import *

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^tscharts/v1/category/', include('category.urls', namespace='category')),
    url(r'^tscharts/v1/clinic/', include('clinic.urls', namespace='clinic')),
    url(r'^tscharts/v1/clinicstation/', include('clinicstation.urls', namespace='clinicstation')),
    url(r'^tscharts/v1/consent/', include('consent.urls', namespace='consent')),
    url(r'^tscharts/v1/image/', include('image.urls', namespace='image')),
    url(r'^tscharts/v1/login/$', LoginView.as_view()),
    url(r'^tscharts/v1/logout/$', LogoutView.as_view()),
    url(r'^tscharts/v1/createuser/$', CreateUserView.as_view()),
    url(r'^tscharts/v1/createuser$', CreateUserView.as_view()),
    url(r'^tscharts/v1/updatepin/$', UpdatePINView.as_view()),
    url(r'^tscharts/v1/updatepassword/$', UpdatePasswordView.as_view()),
    url(r'^tscharts/v1/audiogram/', include('audiogram.urls', namespace='audiogram')),
    url(r'^tscharts/v1/entexam/', include('entexam.urls', namespace='entexam')),
    url(r'^tscharts/v1/entsurgicalhistory/', include('entsurgicalhistory.urls', namespace='entsurgicalhistory')),
    url(r'^tscharts/v1/enthistory/', include('enthistory.urls', namespace='enthistory')),
    url(r'^tscharts/v1/enthistoryextra/', include('enthistoryextra.urls', namespace='enthistoryextra')),
    url(r'^tscharts/v1/enttreatment/', include('enttreatment.urls', namespace='enttreatment')),
    url(r'^tscharts/v1/entdiagnosis/', include('entdiagnosis.urls', namespace='entdiagnosis')),
    url(r'^tscharts/v1/entdiagnosisextra/', include('entdiagnosisextra.urls', namespace='entdiagnosisextra')),
    url(r'^tscharts/v1/dentalcdt/', include('dentalcdt.urls', namespace='dentalcdt')),
    url(r'^tscharts/v1/dentalstate/', include('dentalstate.urls', namespace='dentalstate')),
    url(r'^tscharts/v1/dentaltreatment/', include('dentaltreatment.urls', namespace='dentaltreatment')),
    url(r'^tscharts/v1/medicalhistory/', include('medicalhistory.urls', namespace='medicalhistory')),
    url(r'^tscharts/v1/medications/', include('medications.urls', namespace='medications')),
    url(r'^tscharts/v1/mexicanstates/', include('mexicanstates.urls', namespace='mexicanstates')),
    url(r'^tscharts/v1/patient/', include('patient.urls', namespace='patient')),
    url(r'^tscharts/v1/patient', include('patient.urls', namespace='patient')),
    url(r'^tscharts/v1/queue/', include('queue.urls', namespace='queue')),
    url(r'^tscharts/v1/queueentry/', include('queue.queueentryurls', namespace='queueentry')),
    url(r'^tscharts/v1/register/', include('register.urls', namespace='register')),
    url(r'^tscharts/v1/returntoclinic/', include('returntoclinic.urls', namespace='returntoclinic')),
    url(r'^tscharts/v1/returntoclinicstation/', include('returntoclinicstation.urls', namespace='returntoclinicstation')),
    url(r'^tscharts/v1/routingslip/', include('routingslip.rsurls', namespace='routingslip')),
    url(r'^tscharts/v1/routingslipcomment/', include('routingslip.rscommenturls', namespace='routingslipcomment')),
    url(r'^tscharts/v1/routingslipentry/', include('routingslip.rsentryurls', namespace='routingslipentry')),
    url(r'^tscharts/v1/statechange/', include('statechange.urls', namespace='statechange')),
    url(r'^tscharts/v1/station/', include('station.urls', namespace='station')),
    url(r'^tscharts/v1/surgeryhistory/', include('surgeryhistory.urls', namespace='surgeryhistory')),
    url(r'^tscharts/v1/surgerytype/', include('surgerytype.urls', namespace='surgerytype')),
    url(r'^tscharts/v1/covidvac/', include('covidvac.urls', namespace='covidvac')),
    url(r'^tscharts/v1/vaccine/', include('vaccine.urls', namespace='vaccine')),
    url(r'^tscharts/v1/xray/', include('xray.urls', namespace='xray')),
]

