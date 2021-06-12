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

'''
unit tests for vaccine application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class Vaccine:
    def __init__(self):
        self._covid19 = False
        self._covid19_type = ""
        self._covid19_doses = 0
        self._covid19_date = None
        self._covid19_booster = False
        self._covid19_booster_date  = None
        self._dtap = False
        self._dtap_date  = None
        self._dt = False
        self._dt_date  = None
        self._hib = False
        self._hib_date  = None
        self._hepa = False
        self._hepa_date  = None
        self._hepb = False
        self._hepb_date  = None
        self._hpv = False
        self._hpv_date  = None
        self._iiv = False
        self._iiv_date  = None
        self._laiv4 = False
        self._laiv4_date  = None
        self._mmr = False
        self._mmr_date  = None
        self._menacwy = False
        self._menacwy_date  = None
        self._menb = False
        self._menb_date  = None
        self._pcv13 = False
        self._pcv13_date  = None
        self._ppsv23 = False
        self._ppsv23_date  = None
        self._ipv = False
        self._ipv_date  = None
        self._rv = False
        self._rv_date  = None
        self._tap = False
        self._tap_date  = None
        self._td = False
        self._td_date  = None
        self._varicella = False
        self._varicella_date  = None
        self._dtap_hepb_ipv = False
        self._dtap_hepb_ipv_date  = None
        self._dtap_ipv_hib = False
        self._dtap_ipv_hib_date  = None
        self._dtap_ipv = False
        self._dtap_ipv_date = None
        self._dtap_ipv_hib_hepb = False
        self._dtap_ipv_hib_hepb_date  = None
        self._mmvr = False
        self._mmvr_date  = None

    def toJSON(self):
        ret = {}
        ret["covid19"] = self._covid19
        ret["covid19_doses"] = self._covid19_doses 
        ret["covid19_type"] = self._covid19_type 
        ret["covid19_date"] = self._covid19_date 
        ret["covid19_booster"] = self._covid19_booster
        ret["covid19_booster_date"] = self._covid19_booster_date 
        ret["dtap"] = self._dtap
        ret["dtap_date"] = self._dtap_date 
        ret["dt"] = self._dt
        ret["dt_date"] = self._dt_date
        ret["hib"] = self._hib
        ret["hib_date"] = self._hib_date
        ret["hepa"] = self._hepa
        ret["hepa_date"] = self._hepa_date
        ret["hepb"] = self._hepb
        ret["hepb_date"] = self._hepb_date
        ret["hpv"] = self._hpv
        ret["hpv_date"] = self._hpv_date
        ret["iiv"] = self._iiv
        ret["iiv_date"] = self._iiv_date
        ret["laiv4"] = self._laiv4
        ret["laiv4_date"] = self._laiv4_date
        ret["mmr"] = self._mmr
        ret["mmr_date"] = self._mmr_date
        ret["menacwy"] = self._menacwy
        ret["menacwy_date"] = self._menacwy_date
        ret["menb"] = self._menb
        ret["menb_date"] = self._menb_date 
        ret["pcv13"] = self._pcv13
        ret["pcv13_date"] = self._pcv13_date
        ret["ppsv23"] = self._ppsv23
        ret["ppsv23_date"] = self._ppsv23_date
        ret["ipv"] = self._ipv
        ret["ipv_date"] = self._ipv_date
        ret["rv"] = self._rv
        ret["rv_date"] = self._rv_date
        ret["tap"] = self._tap
        ret["tap_date"] = self._tap_date
        ret["td"] = self._td
        ret["td_date"] = self._td_date
        ret["varicella"] = self._varicella
        ret["varicella_date"] = self._varicella_date 
        ret["dtap_hepb_ipv"] = self._dtap_hepb_ipv
        ret["dtap_hepb_ipv_date"] = self._dtap_hepb_ipv_date
        ret["dtap_ipv_hib"] = self._dtap_ipv_hib
        ret["dtap_ipv_hib_date"] = self._dtap_ipv_hib_date
        ret["dtap_ipv"] = self._dtap_ipv
        ret["dtap_ipv_date"] = self._dtap_ipv_date
        ret["dtap_ipv_hib_hepb"] = self._dtap_ipv_hib_hepb
        ret["dtap_ipv_hib_hepb_date"] = self._dtap_ipv_hib_hepb_date
        ret["mmvr"] = self._mmvr
        ret["mmvr_date"] = self._mmvr_date
        return ret

    def fromJSON(self, data, ignore=True):
        ret = True

        try:
            self.set_covid19(data["covid19"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_covid19_type(data["covid19_type"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_covid19_doses(data["covid19_doses"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_covid19_date(data["covid19_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_covid19_booster(data["covid19_booster"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_covid19_booster_date(data["covid19_booster_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap(data["dtap"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_date(data["dtap_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dt(data["dt"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dt_date(data["dt_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hib(data["hib"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hib_date(data["hib_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hepa(data["hepa"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hepa_date(data["hepa_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hepb(data["hepb"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hepb_date(data["hepb_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hpv(data["hpv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_hpv_date(data["hpv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_iiv(data["iiv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_iiv_date(data["iiv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_laiv4(data["laiv4"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_laiv4_date(data["laiv4_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_mmr(data["mmr"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_mmr_date(data["mmr_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_menacwy(data["menacwy"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_menacwy_date(data["menacwy_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_menb(data["menb"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_menb_date(data["menb_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_pcv13(data["pcv13"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_pcv13_date(data["pcv13_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_ppsv23(data["ppsv23"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_ppsv23_date(data["ppsv23_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_ipv(data["ipv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_ipv_date(data["ipv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_rv(data["rv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_rv_date(data["rv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_tap(data["tap"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_tap_date(data["tap_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_td(data["td"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_td_date(data["td_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_varicella(data["varicella"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_varicella_date(data["varicella_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_hepb_ipv(data["dtap_hepb_ipv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_hepb_ipv_date(data["dtap_hepb_ipv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv_hib(data["dtap_ipv_hib"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv_hib_date(data["dtap_ipv_hib_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv(data["dtap_ipv"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv_date(data["dtap_ipv_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv_hib_hepb(data["dtap_ipv_hib_hepb"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_dtap_ipv_hib_hepb_date(data["dtap_ipv_hib_hepb_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_mmvr(data["mmvr"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        try:
            self.set_mmvr_date(data["mmvr_date"])
        except:
            if ignore: 
                pass 
            else: 
                ret = False 
        return ret

    def set_covid19(self, val):
        self._covid19 = val

    def set_covid19_doses(self, val):
        self._covid19_doses = val

    def set_covid19_type(self, val):
        self._covid19_type = val

    def set_covid19_date(self, val):
        self._covid19_date= val

    def set_covid19_booster(self, val):
        self._covid19_booster = val

    def set_covid19_booster_date(self, val):
        self._covid19_booster_date = val

    def set_dtap(self, val):
        self._dtap = val

    def set_dtap_date(self, val):
        self._dtap_date = val

    def set_dt(self, val):
        self._dt = val

    def set_dt_date(self, val):
        self._dt_date = val

    def set_hib(self, val):
        self._hib = val

    def set_hib_date(self, val):
        self._hib_date = val

    def set_hepa(self, val):
        self._hepa = val

    def set_hepa_date(self, val):
        self._hepa_date = val

    def set_hepb(self, val):
        self._hepb = val

    def set_hepb_date(self, val):
        self._hepb_date = val

    def set_hpv(self, val):
        self._hpv = val

    def set_hpv_date(self, val):
        self._hpv_date = val

    def set_iiv(self, val):
        self._iiv = val

    def set_iiv_date(self, val):
        self._iiv_date = val

    def set_laiv4(self, val):
        self._laiv4 = val

    def set_laiv4_date(self, val):
        self._laiv4_date = val

    def set_mmr(self, val):
        self._mmr = val

    def set_mmr_date(self, val):
        self._mmr_date = val

    def set_menacwy(self, val):
        self._menacwy = val

    def set_menacwy_date(self, val):
        self._menacwy_date = val

    def set_menb(self, val):
        self._menb = val

    def set_menb_date(self, val):
        self._menb_date = val

    def set_pcv13(self, val):
        self._pcv13 = val

    def set_pcv13_date(self, val):
        self._pcv13_date = val

    def set_ppsv23(self, val):
        self._ppsv23 = val

    def set_ppsv23_date(self, val):
        self._ppsv23_date = val

    def set_ipv(self, val):
        self._ipv = val

    def set_ipv_date(self, val):
        self._ipv_date = val

    def set_rv(self, val):
        self._rv = val

    def set_rv_date(self, val):
        self._rv_date = val

    def set_tap(self, val):
        self._tap = val

    def set_tap_date(self, val):
        self._tap_date = val

    def set_td(self, val):
        self._td = val

    def set_td_date(self, val):
        self._td_date = val

    def set_varicella(self, val):
        self._varicella = val

    def set_varicella_date(self, val):
        self._varicella_date = val

    def set_dtap_hepb_ipv(self, val):
        self._dtap_hepb_ipv = val

    def set_dtap_hepb_ipv_date(self, val):
        self._dtap_hepb_ipv_date = val

    def set_dtap_ipv_hib(self, val):
        self._dtap_ipv_hib = val

    def set_dtap_ipv_hib_date(self, val):
        self._dtap_ipv_hib_date = val

    def set_dtap_ipv(self, val):
        self._dtap_ipv = val

    def set_dtap_ipv_date(self, val):
        self._dtap_ipv_date= val

    def set_dtap_ipv_hib_hepb(self, val):
        self._dtap_ipv_hib_hepb = val

    def set_dtap_ipv_hib_hepb_date(self, val):
        self._dtap_ipv_hib_hepb_date = val

    def set_mmvr(self, val):
        self._mmvr = val

    def set_mmvr_date(self, val):
        self._mmvr_date = val

    def get_covid19(self):
        return self._covid19

    def get_covid19_type(self):
        return self._covid19_type

    def get_covid19_doses(self):
        return self._covid19_doses

    def get_covid19_date(self):
        return self._covid19_date

    def get_covid19_booster(self):
        return self._covid19_booster

    def get_covid19_booster_date(self):
        return self._covid19_booster_date

    def get_dtap(self):
        return self._dtap

    def get_dtap_date(self):
        return self._dtap_date

    def get_dt(self):
        return self._dt

    def get_dt_date(self):
        return self._dt_date

    def get_hib(self):
        return self._hib

    def get_hib_date(self):
        return self._hib_date

    def get_hepa(self):
        return self._hepa

    def get_hepa_date(self):
        return self._hepa_date

    def get_hepb(self):
        return self._hepb

    def get_hepb_date(self):
        return self._hepb_date 

    def get_hpv(self):
        return self._hpv

    def get_hpv_date(self):
        return self._hpv_date 

    def get_iiv(self):
        return self._iiv 

    def get_iiv_date(self):
        return self._iiv_date 

    def get_laiv4(self):
        return self._laiv4 

    def get_laiv4_date(self):
        return self._laiv4_date 

    def get_mmr(self):
        return self._mmr 

    def get_mmr_date(self):
        return self._mmr_date 

    def get_menacwy(self):
        return self._menacwy 

    def get_menacwy_date(self):
        return self._menacwy_date 

    def get_menb(self):
        return self._menb

    def get_menb_date(self):
        return self._menb_date 

    def get_pcv13(self):
        return self._pcv13 

    def get_pcv13_date(self):
        return self._pcv13_date 

    def get_ppsv23(self):
        return self._ppsv23 

    def get_ppsv23_date(self):
        return self._ppsv23_date 

    def get_ipv(self):
        return self._ipv 

    def get_ipv_date(self):
        return self._ipv_date 

    def get_rv(self):
        return self._rv 

    def get_rv_date(self):
        return self._rv_date 

    def get_tap(self):
        return self._tap 

    def get_tap_date(self):
        return self._tap_date 

    def get_td(self):
        return self._td 

    def get_td_date(self):
        return self._td_date 

    def get_varicella(self):
        return self._varicella 

    def get_varicella_date(self):
        return self._varicella_date 

    def get_dtap_hepb_ipv(self):
        return self._dtap_hepb_ipv 

    def get_dtap_hepb_ipv_date(self):
        return self._dtap_hepb_ipv_date 

    def get_dtap_ipv_hib(self):
        return self._dtap_ipv_hib 

    def get_dtap_ipv_hib_date(self):
        return self._dtap_ipv_hib_date 

    def get_dtap_ipv(self):
        return self._dtap_ipv 

    def get_dtap_ipv_date(self):
        return self._dtap_ipv_date

    def get_dtap_ipv_hib_hepb(self):
        return self._dtap_ipv_hib_hepb 

    def get_dtap_ipv_hib_hepb_date(self):
        return self._dtap_ipv_hib_hepb_date 

    def get_mmvr(self):
        return self._mmvr 

    def get_mmvr_date(self):
        return self._mmvr_date 

class CreateVaccine(ServiceAPI):
    def __init__(self, host, port, token, clinic, patient):
        super(CreateVaccine, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {"patient": patient, "clinic": clinic}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/vaccine/")
        self._v  = Vaccine()

    def setVaccine(self, vaccine):
        for k, v in vaccine.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class GetVaccine(ServiceAPI):

    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/vaccine/{}/".format(self._id)
        else:
            base = "tscharts/v1/vaccine/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetVaccine, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._patient = None
        self._id = None
        self.makeURL()
        self._v  = Vaccine()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setPatient(self, patient):
        self._patient = patient
        self.makeURL()

class UpdateVaccine(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateVaccine, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = self.getPayload()
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/vaccine/{}/".format(id))
        self._v  = Vaccine()

    def setVaccine(self, vaccine):
        for k, v in vaccine.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class DeleteVaccine(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteVaccine, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/vaccine/{}/".format(id))

class TestTSVaccine(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateVaccineNoneDate(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid, clinic=clinicid)

        x._v.set_covid19(True)
        x._v.set_covid19_doses(1)
        x._v.set_covid19_type("Moderna")
        x._v.set_covid19_date("01/01/1901")
        x._v.set_covid19_booster(False)
        x._v.set_covid19_booster_date(None)
        x._v.set_dtap(True)
        x._v.set_dtap_date("01/01/1903")
        x._v.set_dt(False)
        x._v.set_dt_date(None)
        x._v.set_hib(True)
        x._v.set_hib_date("01/01/1905")
        x._v.set_hepa(False)
        x._v.set_hepa_date(None)
        x._v.set_hepb(True)
        x._v.set_hepb_date("01/01/1907")
        x._v.set_hpv(False)
        x._v.set_hpv_date(None)
        x._v.set_iiv(True)
        x._v.set_iiv_date("01/01/1909")
        x._v.set_laiv4(False)
        x._v.set_laiv4_date(None)
        x._v.set_mmr(True)
        x._v.set_mmr_date("01/01/1911")
        x._v.set_menacwy(False)
        x._v.set_menacwy_date(None)
        x._v.set_menb(True)
        x._v.set_menb_date("01/01/1913")
        x._v.set_pcv13(False)
        x._v.set_pcv13_date(None)
        x._v.set_ppsv23(True)
        x._v.set_ppsv23_date("01/01/1915")
        x._v.set_ipv(False)
        x._v.set_ipv_date(None)
        x._v.set_rv(True)
        x._v.set_rv_date("01/01/1917")
        x._v.set_tap(False)
        x._v.set_tap_date(None)
        x._v.set_td(True)
        x._v.set_td_date("01/01/1919")
        x._v.set_varicella(False)
        x._v.set_varicella_date(None)
        x._v.set_dtap_hepb_ipv(True)
        x._v.set_dtap_hepb_ipv_date("01/01/1921")
        x._v.set_dtap_ipv_hib(False)
        x._v.set_dtap_ipv_hib_date(None)
        x._v.set_dtap_ipv(True)
        x._v.set_dtap_ipv_date("01/01/1923")
        x._v.set_dtap_ipv_hib_hepb(False)
        x._v.set_dtap_ipv_hib_hepb_date(None)
        x._v.set_mmvr(True)
        x._v.set_mmvr_date("01/01/1925")

        data = x._v.toJSON()

        x.setVaccine(data)
 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data2 = ret[1]

        for key, value in data.items():
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        x = GetVaccine(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data2 = ret[1]

        for key, value in data.items(): 
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        x = DeleteVaccine(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateVaccine(host, port, token, clinic=9999, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data, boolean arg

        x._v._mmvr = 9999

        data = x._v.toJSON()
        x.setVaccine(data)

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateVaccine(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid, clinic=clinicid)

        x._v.set_covid19(True)
        x._v.set_covid19_doses(1)
        x._v.set_covid19_type("Moderna")
        x._v.set_covid19_date("01/01/1901")
        x._v.set_covid19_booster(False)
        x._v.set_covid19_booster_date("01/01/1902")
        x._v.set_dtap(True)
        x._v.set_dtap_date("01/01/1903")
        x._v.set_dt(False)
        x._v.set_dt_date("01/01/1904")
        x._v.set_hib(True)
        x._v.set_hib_date("01/01/1905")
        x._v.set_hepa(False)
        x._v.set_hepa_date("01/01/1906")
        x._v.set_hepb(True)
        x._v.set_hepb_date("01/01/1907")
        x._v.set_hpv(False)
        x._v.set_hpv_date("01/01/1908")
        x._v.set_iiv(True)
        x._v.set_iiv_date("01/01/1909")
        x._v.set_laiv4(False)
        x._v.set_laiv4_date("01/01/1910")
        x._v.set_mmr(True)
        x._v.set_mmr_date("01/01/1911")
        x._v.set_menacwy(False)
        x._v.set_menacwy_date("01/01/1912")
        x._v.set_menb(True)
        x._v.set_menb_date("01/01/1913")
        x._v.set_pcv13(False)
        x._v.set_pcv13_date("01/01/1914")
        x._v.set_ppsv23(True)
        x._v.set_ppsv23_date("01/01/1915")
        x._v.set_ipv(False)
        x._v.set_ipv_date("01/01/1916")
        x._v.set_rv(True)
        x._v.set_rv_date("01/01/1917")
        x._v.set_tap(False)
        x._v.set_tap_date("01/01/1918")
        x._v.set_td(True)
        x._v.set_td_date("01/01/1919")
        x._v.set_varicella(False)
        x._v.set_varicella_date("01/01/1920")
        x._v.set_dtap_hepb_ipv(True)
        x._v.set_dtap_hepb_ipv_date("01/01/1921")
        x._v.set_dtap_ipv_hib(False)
        x._v.set_dtap_ipv_hib_date("01/01/1922")
        x._v.set_dtap_ipv(True)
        x._v.set_dtap_ipv_date("01/01/1923")
        x._v.set_dtap_ipv_hib_hepb(False)
        x._v.set_dtap_ipv_hib_hepb_date("01/01/1924")
        x._v.set_mmvr(True)
        x._v.set_mmvr_date("01/01/1925")

        data = x._v.toJSON()

        x.setVaccine(data)
 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data2 = ret[1]

        for key, value in data.items():
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        x = GetVaccine(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data2 = ret[1]

        for key, value in data.items(): 
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        x = DeleteVaccine(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateVaccine(host, port, token, clinic=9999, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data, boolean arg

        x._v._mmvr = 9999

        data = x._v.toJSON()
        x.setVaccine(data)

        x = CreateVaccine(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteVaccine(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid, clinic=clinicid)
        x._v.set_covid19(True)
        x._v.set_covid19_doses(1)
        x._v.set_covid19_type("Moderna")
        x._v.set_covid19_date("01/01/1901")
        x._v.set_covid19_booster(False)
        x._v.set_covid19_booster_date("01/01/1902")
        x._v.set_dtap(True)
        x._v.set_dtap_date("01/01/1903")
        x._v.set_dt(False)
        x._v.set_dt_date("01/01/1904")
        x._v.set_hib(True)
        x._v.set_hib_date("01/01/1905")
        x._v.set_hepa(False)
        x._v.set_hepa_date("01/01/1906")
        x._v.set_hepb(True)
        x._v.set_hepb_date("01/01/1907")
        x._v.set_hpv(False)
        x._v.set_hpv_date("01/01/1908")
        x._v.set_iiv(True)
        x._v.set_iiv_date("01/01/1909")
        x._v.set_laiv4(False)
        x._v.set_laiv4_date("01/01/1910")
        x._v.set_mmr(True)
        x._v.set_mmr_date("01/01/1911")
        x._v.set_menacwy(False)
        x._v.set_menacwy_date("01/01/1912")
        x._v.set_menb(True)
        x._v.set_menb_date("01/01/1913")
        x._v.set_pcv13(False)
        x._v.set_pcv13_date("01/01/1914")
        x._v.set_ppsv23(True)
        x._v.set_ppsv23_date("01/01/1915")
        x._v.set_ipv(False)
        x._v.set_ipv_date("01/01/1916")
        x._v.set_rv(True)
        x._v.set_rv_date("01/01/1917")
        x._v.set_tap(False)
        x._v.set_tap_date("01/01/1918")
        x._v.set_td(True)
        x._v.set_td_date("01/01/1919")
        x._v.set_varicella(False)
        x._v.set_varicella_date("01/01/1920")
        x._v.set_dtap_hepb_ipv(True)
        x._v.set_dtap_hepb_ipv_date("01/01/1921")
        x._v.set_dtap_ipv_hib(False)
        x._v.set_dtap_ipv_hib_date("01/01/1922")
        x._v.set_dtap_ipv(True)
        x._v.set_dtap_ipv_date("01/01/1923")
        x._v.set_dtap_ipv_hib_hepb(False)
        x._v.set_dtap_ipv_hib_hepb_date("01/01/1924")
        x._v.set_mmvr(True)
        x._v.set_mmvr_date("01/01/1925")

        data = x._v.toJSON()

        x.setVaccine(data)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteVaccine(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteVaccine(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteVaccine(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteVaccine(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteVaccine(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateVaccine(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid, clinic=clinicid)
        x._v.set_covid19(True)
        x._v.set_covid19_doses(1)
        x._v.set_covid19_type("Moderna")
        x._v.set_covid19_date("01/01/1901")
        x._v.set_covid19_booster(False)
        x._v.set_covid19_booster_date("01/01/1902")
        x._v.set_dtap(True)
        x._v.set_dtap_date("01/01/1903")
        x._v.set_dt(False)
        x._v.set_dt_date("01/01/1904")
        x._v.set_hib(True)
        x._v.set_hib_date("01/01/1905")
        x._v.set_hepa(False)
        x._v.set_hepa_date("01/01/1906")
        x._v.set_hepb(True)
        x._v.set_hepb_date("01/01/1907")
        x._v.set_hpv(False)
        x._v.set_hpv_date("01/01/1908")
        x._v.set_iiv(True)
        x._v.set_iiv_date("01/01/1909")
        x._v.set_laiv4(False)
        x._v.set_laiv4_date("01/01/1910")
        x._v.set_mmr(True)
        x._v.set_mmr_date("01/01/1911")
        x._v.set_menacwy(False)
        x._v.set_menacwy_date("01/01/1912")
        x._v.set_menb(True)
        x._v.set_menb_date("01/01/1913")
        x._v.set_pcv13(False)
        x._v.set_pcv13_date("01/01/1914")
        x._v.set_ppsv23(True)
        x._v.set_ppsv23_date("01/01/1915")
        x._v.set_ipv(False)
        x._v.set_ipv_date("01/01/1916")
        x._v.set_rv(True)
        x._v.set_rv_date("01/01/1917")
        x._v.set_tap(False)
        x._v.set_tap_date("01/01/1918")
        x._v.set_td(True)
        x._v.set_td_date("01/01/1919")
        x._v.set_varicella(False)
        x._v.set_varicella_date("01/01/1920")
        x._v.set_dtap_hepb_ipv(True)
        x._v.set_dtap_hepb_ipv_date("01/01/1921")
        x._v.set_dtap_ipv_hib(False)
        x._v.set_dtap_ipv_hib_date("01/01/1922")
        x._v.set_dtap_ipv(True)
        x._v.set_dtap_ipv_date("01/01/1923")
        x._v.set_dtap_ipv_hib_hepb(False)
        x._v.set_dtap_ipv_hib_hepb_date("01/01/1924")
        x._v.set_mmvr(True)
        x._v.set_mmvr_date("01/01/1925")

        data = x._v.toJSON()

        x.setVaccine(data)
 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data2 = ret[1]
        for key, value in data.items():
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        data["mmvr_date"] = "01/01/1934"
        data["mmvr"] = False

        x = UpdateVaccine(host, port, token, id)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data2 = ret[1]
        for key, value in data.items(): 
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])

        # test update date to None

        data["mmvr_date"] = None 
        data["mmvr"] = False 

        x = UpdateVaccine(host, port, token, id)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data2 = ret[1]
        for key, value in data.items(): 
            self.assertTrue(key in data2)
            self.assertTrue(data2[key] == data[key])


        data["hepititis"] = "Hello" 
        data["pregnancy_duration"] = 8 
        data["parents_cleft"] = True 
        x = UpdateVaccine(host, port, token, id)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = False 
        data["pregnancy_duration"] = 3 
        data["parents_cleft"] = True 
        x = UpdateVaccine(host, port, token, id)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteVaccine(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllVaccines(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid1 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "05/05/2016", "05/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid2 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "08/05/2016", "08/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid3 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "3abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid1 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "1abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "2abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        delids = []

        x = CreateVaccine(host, port, token, patient=patientid1, clinic=clinicid1)
        x._v.set_covid19(True)
        x._v.set_covid19_doses(1)
        x._v.set_covid19_type("Moderna")
        x._v.set_covid19_date("01/01/1901")
        x._v.set_covid19_booster(False)
        x._v.set_covid19_booster_date("01/01/1902")
        x._v.set_dtap(True)
        x._v.set_dtap_date("01/01/1903")
        x._v.set_dt(False)
        x._v.set_dt_date("01/01/1904")
        x._v.set_hib(True)
        x._v.set_hib_date("01/01/1905")
        x._v.set_hepa(False)
        x._v.set_hepa_date("01/01/1906")
        x._v.set_hepb(True)
        x._v.set_hepb_date("01/01/1907")
        x._v.set_hpv(False)
        x._v.set_hpv_date("01/01/1908")
        x._v.set_iiv(True)
        x._v.set_iiv_date("01/01/1909")
        x._v.set_laiv4(False)
        x._v.set_laiv4_date("01/01/1910")
        x._v.set_mmr(True)
        x._v.set_mmr_date("01/01/1911")
        x._v.set_menacwy(False)
        x._v.set_menacwy_date("01/01/1912")
        x._v.set_menb(True)
        x._v.set_menb_date("01/01/1913")
        x._v.set_pcv13(False)
        x._v.set_pcv13_date("01/01/1914")
        x._v.set_ppsv23(True)
        x._v.set_ppsv23_date("01/01/1915")
        x._v.set_ipv(False)
        x._v.set_ipv_date("01/01/1916")
        x._v.set_rv(True)
        x._v.set_rv_date("01/01/1917")
        x._v.set_tap(False)
        x._v.set_tap_date("01/01/1918")
        x._v.set_td(True)
        x._v.set_td_date("01/01/1919")
        x._v.set_varicella(False)
        x._v.set_varicella_date("01/01/1920")
        x._v.set_dtap_hepb_ipv(True)
        x._v.set_dtap_hepb_ipv_date("01/01/1921")
        x._v.set_dtap_ipv_hib(False)
        x._v.set_dtap_ipv_hib_date("01/01/1922")
        x._v.set_dtap_ipv(True)
        x._v.set_dtap_ipv_date("01/01/1923")
        x._v.set_dtap_ipv_hib_hepb(False)
        x._v.set_dtap_ipv_hib_hepb_date("01/01/1924")
        x._v.set_mmvr(True)
        x._v.set_mmvr_date("01/01/1925")

        data = x._v.toJSON()

        x.setVaccine(data)
 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid2, clinic=clinicid1)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid3, clinic=clinicid1)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid1, clinic=clinicid2)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid2, clinic=clinicid2)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid3, clinic=clinicid2)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid1, clinic=clinicid3)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid2, clinic=clinicid3)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateVaccine(host, port, token, patient=patientid3, clinic=clinicid3)
        x.setVaccine(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetVaccine(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetVaccine(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetVaccine(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetVaccine(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetVaccine(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetVaccine(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteVaccine(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetVaccine(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = DeleteClinic(host, port, token, clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("vaccine [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    global host
    host = "127.0.0.1"
    global port
    port = 8000
    global username
    username = None
    global password
    password = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
