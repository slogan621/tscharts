# -*- coding: utf-8 -*-

#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
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

from __future__ import unicode_literals

from django.db import models

from patient.models import Patient
from clinic.models import Clinic

class Vaccine(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    time = models.DateTimeField(auto_now=True)

    covid19 = models.BooleanField(default = False) # COVID-19
    covid19_doses = models.IntegerField(default=0) # 0, 1 or 2
    covid19_date = models.DateTimeField(null=True)
    covid19_booster = models.BooleanField(default = False) # COVID-19
    covid19_booster_date = models.DateTimeField(null=True)
    dtap = models.BooleanField(default = False) #Diphtheria, tetanus, and acellular pertussis vaccine 
    dtap_date = models.DateTimeField(null=True)
    dt = models.BooleanField(default = False) #Diphtheria, tetanus vaccine
    dt_date = models.DateTimeField(null=True)
    hib = models.BooleanField(default = False) #Haemophilus influenzae type B vaccine
    hib_date = models.DateTimeField(null=True)
    hepa = models.BooleanField(default = False) #Hepatitis A vaccine
    hepa_date = models.DateTimeField(null=True)
    hepb = models.BooleanField(default = False) #Hepatitis B vaccine
    hepb_date = models.DateTimeField(null=True)
    hpv = models.BooleanField(default = False) #Human papillomavirus vaccine
    hpv_date = models.DateTimeField(null=True)
    iiv = models.BooleanField(default = False) #Influenza vaccine (inactivated)
    iiv_date = models.DateTimeField(null=True)
    laiv4 = models.BooleanField(default = False) #Influenza vaccine (live, attenuated)
    laiv4_date = models.DateTimeField(null=True)
    mmr = models.BooleanField(default = False) #Measles, mumps, and rubella vaccine
    mmr_date = models.DateTimeField(null=True)
    menacwy = models.BooleanField(default = False) #Meningococcal serogroups A, C, W, Y vaccine
    menacwy_date = models.DateTimeField(null=True)
    menb = models.BooleanField(default = False) #Meningococcal serogroup B vaccine
    menb_date = models.DateTimeField(null=True)
    pcv13 = models.BooleanField(default = False) #Pneumococcal 13-valent conjugate vaccine
    pcv13_date = models.DateTimeField(null=True)
    ppsv23 = models.BooleanField(default = False) #Pneumococcal 23-valent polysaccharide vaccine
    ppsv23_date = models.DateTimeField(null=True)
    ipv = models.BooleanField(default = False) #Poliovirus vaccine (inactivated)
    ipv_date = models.DateTimeField(null=True)
    rv = models.BooleanField(default = False) #Rotavirus vaccine
    rv_date = models.DateTimeField(null=True)
    tap = models.BooleanField(default = False) #Tetanus, diphtheria, and acellular pertussis vaccine
    tap_date = models.DateTimeField(null=True)
    td = models.BooleanField(default = False) #Tetanus and diphtheria vaccine
    td_date = models.DateTimeField(null=True)
    varicella = models.BooleanField(default = False) #Varicella vaccine
    varicella_date = models.DateTimeField(null=True)
    dtap_hepb_ipv = models.BooleanField(default = False) #DTaP, hepatitis B, and inactivated poliovirus vaccine
    dtap_hepb_ipv_date = models.DateTimeField(null=True)
    dtap_ipv_hib = models.BooleanField(default = False) #DTaP, inactivated poliovirus, and Haemophilus influenzae type B vaccine
    dtap_ipv_hib_date = models.DateTimeField(null=True)
    dtap_ipv = models.BooleanField(default = False) #DTaP and inactivated poliovirus vaccine
    dtap_ipv_date = models.DateTimeField(null=True)
    dtap_ipv_hib_hepb = models.BooleanField(default = False) #DTaP, inactivated poliovirus, Haemophilus influenzae type b, and hepatitis B vaccine
    dtap_ipv_hib_hepb_date = models.DateTimeField(null=True)
    mmvr = models.BooleanField(default = False) #Measles, mumps, rubella, and varicella vaccines
    mmvr_date = models.DateTimeField(null=True)
