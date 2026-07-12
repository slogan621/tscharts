#(C) Copyright Syd Logan 2020-2026
#(C) Copyright Thousand Smiles Foundation 2020-2026
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

from django.urls import re_path
from audiogram.views import AudiogramView

urlpatterns = [
    re_path(r'^$', AudiogramView.as_view()),
    re_path(r'^([0-9]+)/$', AudiogramView.as_view()),
]
