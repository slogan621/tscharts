#(C) Copyright Syd Logan 2020
#(C) Copyright Thousand Smiles Foundation 2020
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

import getopt, sys
import json
import time
import wx

from advanced_search import AdvancedSearch
from regular_search import RegularSearch
from imagegrid import ImageGrid
from photoctrl import PhotoCtrl
from pubsub import pub

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.register.register import GetAllRegistrations
from test.patient.patient import GetPatient
from test.clinic.clinic import GetAllClinics
from test.image.image import GetImage
from collections import OrderedDict

class TSSession():
    def __init__(self):
        self.m_host = "127.0.0.1"
        self.m_port = 443
        self.m_username = ""
        self.m_password = ""
        self.m_token = ""

    def setHost(self, host):
        self.m_host = host

    def getHost(self):
        return self.m_host

    def setPort(self, port):
        self.m_port = port

    def getPort(self):
        return self.m_port

    def setUsername(self, username):
        self.m_username = username

    def getUsername(self):
        return self.m_username

    def setPassword(self, password):
        self.m_password = password

    def getPassword(self):
        return self.m_password

    def setToken(self, token):
        self.m_token = token

    def getToken(self):
        return self.m_token

    def login(self):
        retval = True
        login = Login(self.getHost(), self.getPort(), self.getUsername(),
self.getPassword())
        ret = login.send(timeout=30)
        if ret[0] != 200:
            print("failed to login: {}".format(ret[1]))
            retval = False
        else:
            self.setToken(ret[1]["token"])
        return retval

class Clinics():
    def getAllClinics(self, sess):
        x = GetAllClinics(sess.getHost(), sess.getPort(), sess.getToken())
        ret = x.send(timeout=30)
        if ret[0] == 200:
            tmp = []
            for x in ret[1]:
                #tmp.append((x["id"], "Clinic Number: {} Location: {} Start: {} End: {}".format(x["id"], x["location"], x["start"], x["end"])))
                tmp.append(x)
            ret = sorted(tmp, key = lambda i: i['start'], reverse=True) 
        else:
            ret = None
        return ret

class Registrations():

    def getPatient(self, sess, id):
        x = GetPatient(sess.getHost(), sess.getPort(), sess.getToken())
        x.setId(id)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            ret = ret[1]
        else:
            ret = None
        return ret

    def searchPatient(self, sess, pattern):
        x = GetPatient(sess.getHost(), sess.getPort(), sess.getToken())
        x.setPaternalLast(pattern)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            ret = ret[1]
        else:
            ret = None
        return ret

    def getAllRegistrations(self, sess, clinicid):
        patients = []
        x = GetAllRegistrations(sess.getHost(), sess.getPort(), sess.getToken())
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            registrations = ret[1]
            for x in registrations:
                y = self.getPatient(sess, x["patient"])
                if y:
                    p = {}
                    p["id"] = y["id"]
                    p["first"] = y["first"]
                    p["middle"] = y["middle"]
                    p["paternal_last"] = y["paternal_last"]
                    p["maternal_last"] = y["maternal_last"]
                    p["dob"] = y["dob"]
                    p["gender"] = y["gender"]
                    patients.append(p)
        return patients

    def searchAllRegistrations(self, sess, clinicid, pattern):
        patients = []
        matches = self.searchPatient(sess, pattern)
        print("matches: {}", matches)
        x = GetAllRegistrations(sess.getHost(), sess.getPort(), sess.getToken())
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            registrations = ret[1]
            for x in registrations:
                if x["patient"] in matches:
                    y = self.getPatient(sess, x["patient"])
                    if y:
                        p = {}
                        p["id"] = y["id"]
                        p["first"] = y["first"]
                        p["middle"] = y["middle"]
                        p["paternal_last"] = y["paternal_last"]
                        p["maternal_last"] = y["maternal_last"]
                        p["dob"] = y["dob"]
                        p["gender"] = y["gender"]
                        patients.append(p)
        return patients

def usage():
    print("xrayuploader [-h host] [-p port] -u username -w password") 

class MainPanel(wx.Panel):

    def __init__(self, parent, sess, clinics):
        super().__init__(parent)
        self.sess = sess
        self.search_term = None
        pub.subscribe(self.update_ui, 'update_ui')
        pub.subscribe(self.on_disable_upload_message, 'disableupload')
        pub.subscribe(self.on_enable_upload_message, 'enableupload')

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        search_sizer = wx.BoxSizer()
        clinics_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_sizer = wx.BoxSizer(wx.HORIZONTAL)

        txt = 'Select Clinic and Patient'
        label = wx.StaticText(self, label=txt)
        self.main_sizer.Add(label, 0, wx.ALL, 5)
        self.clinicIds = []
        for x in clinics:
            self.clinicIds.append(x["id"])
        self.clinics = wx.ListCtrl(self, size=(-1, -1), style=wx.LC_REPORT)
        
        self.clinics.InsertColumn(0, "Clinic Number")
        self.clinics.InsertColumn(1, "Location")
        self.clinics.InsertColumn(2, "Start")
        self.clinics.InsertColumn(3, "End")

        index = 0
        for i in clinics: 
            self.clinics.InsertStringItem(index, str(i["id"])) 
            self.clinics.SetStringItem(index, 1, i["location"]) 
            self.clinics.SetStringItem(index, 2, i["start"])
            self.clinics.SetStringItem(index, 3, i["end"])
            index += 1

        self.clinics.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_clinic, self.clinics)
        clinics_sizer.Add(self.clinics, 1, wx.EXPAND)
        self.search = wx.SearchCtrl(
            self, style=wx.TE_PROCESS_ENTER, size=(-1, 25))
        self.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.on_search)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        search_sizer.Add(self.search, 1, wx.EXPAND)
        
        self.main_sizer.Add(clinics_sizer, 0, wx.ALL|wx.EXPAND, 5)
        self.main_sizer.Add(search_sizer, 0, wx.EXPAND)

        self.search_panel = RegularSearch(self, sess)
        #self.advanced_search_panel = AdvancedSearch(self)
        #self.advanced_search_panel.Hide()
        self.main_sizer.Add(self.search_panel, 1, wx.ALL | wx.EXPAND)

        self.photo_ctrl = PhotoCtrl(parent=self, sess=self.sess)
        image_sizer.Add(self.photo_ctrl, 0, wx.LEFT, 5)

        self.upload_btn = wx.Button(self, label='Upload X-Ray')
        self.upload_btn.Disable()
        self.upload_btn.Bind(wx.EVT_BUTTON, self.on_upload)
        image_sizer.Add(self.upload_btn, 0, wx.LEFT, 5)

        image_sizer.Add((20,-1), proportion=1)  # this is a spacer
        self.imagegrid = ImageGrid(parent=self)
        image_sizer.Add(self.imagegrid, 0, wx.ALL, 5)
        self.main_sizer.Add(image_sizer, 0, wx.ALL)

        #self.main_sizer.Add(self.advanced_search_panel, 1, wx.EXPAND)

        self.SetSizer(self.main_sizer)
        pub.subscribe(self.on_refresh_message, 'refresh')
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timerHandler, self.timer)
        self.timer.Start(60000)

    def timerHandler(self, event):
        print("updated: {}".format(time.ctime()))
        self.on_search(None)
        pub.sendMessage('patients_updated')

    def on_refresh_message(self):
        print("on_refresh_message")
        self.Layout()

    def setClinic(self, id):
        self.clinic = id

    def on_disable_upload_message(self):
        self.upload_btn.Disable()

    def on_enable_upload_message(self):
        self.upload_btn.Enable()

    def on_upload(self, event):
        filepath = self.photo_ctrl.get_image_path()
        self.imagegrid.add(filepath)
        pub.sendMessage('disableupload')
        pub.sendMessage("clearxraycontrol")
        pub.sendMessage('refresh')

    def set_registrations(self, registrations):
        self.search_panel.load_search_results(registrations)

    def on_clinic(self, event):
        ind = event.GetIndex()
        item = self.clinics.GetItem(ind, 0)
        regs = Registrations()
        self.clinic = int(item.GetText())
        patientsThisClinic = regs.getAllRegistrations(self.sess, self.clinic)
        self.set_registrations(patientsThisClinic)
        if len(patientsThisClinic):
            self.search_panel.update_image(int(patientsThisClinic[0]["id"]))

    def on_search(self, event):
        print("on search enter")
        search_results = []
        if event:
            self.search_term = event.GetString()
        regs = Registrations()
        if self.search_term and len(self.search_term):
            patientsThisClinic = regs.searchAllRegistrations(self.sess,
self.clinic, self.search_term)
        else:
            patientsThisClinic = regs.getAllRegistrations(self.sess, self.clinic)
        self.set_registrations(patientsThisClinic)
        if len(patientsThisClinic):
            self.search_panel.update_image(int(patientsThisClinic[0]["id"]))

    def on_advanced_search(self, event):
        self.search.Hide()
        self.search_panel.Hide()
        self.advanced_search_btn.Hide()
        self.advanced_search_panel.Show()
        self.main_sizer.Layout()

    def update_ui(self):
        """
        Hide advanced search and re-show original screen

        Called by pubsub when advanced search is invoked
        """
        self.advanced_search_panel.Hide()
        self.search.Show()
        self.search_panel.Show()
        self.advanced_search_btn.Show()
        self.main_sizer.Layout()

class SearchFrame(wx.Frame):

    def __init__(self, sess, clinics):
        super().__init__(None, title='X-Ray Uploader',
                         size=(1200, 800))
        panel = MainPanel(self, sess, clinics)
        self.Show()
        regs = Registrations()
        print("{}".format(clinics))
        patientsThisClinic = regs.getAllRegistrations(sess, clinics[0]["id"])
        panel.setClinic(int(clinics[0]["id"]))
        panel.set_registrations(patientsThisClinic)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    session = TSSession()
    host = "127.0.0.1"
    port = 8000
    username = None
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
    session.setHost(host)
    session.setPort(port)
    session.setUsername(username)
    session.setPassword(password)
    if session.login() == False:
        exit(1)
    regs = Registrations()
    c = Clinics()
    clinics = c.getAllClinics(session)
    for x in clinics:
        print("{}".format(x))   
   
    clinicid = int(clinics[0]["id"])

    '''
    patientsThisClinic = regs.getAllRegistrations(session, clinicid)
    for x in patientsThisClinic:
        print("{}".format(x))   
    '''

    app = wx.App(False)
    frame = SearchFrame(session, clinics)
    app.MainLoop()

if __name__ == "__main__":
    main()
