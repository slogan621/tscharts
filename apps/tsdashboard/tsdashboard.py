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
import base64
import tempfile
import os

from regular_search import RegularSearch
from imagegrid import ImageGrid
from photoctrl import PhotoCtrl
from pubsub import pub

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.register.register import GetAllRegistrations
from tschartslib.patient.patient import GetPatient
from tschartslib.clinic.clinic import GetAllClinics
from tschartslib.image.image import GetImage, CreateImage, DeleteImage
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
        login = Login(self.getHost(), self.getPort(), 
                      self.getUsername(), self.getPassword())
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

class XRays():

    def getAllXRays(self, sess, clinicid, patientid):
        xrays = []
        x = GetImage(sess.getHost(), sess.getPort(), sess.getToken())
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setType("Xray")
        ret = x.send(timeout=30)
        print("getAllXRays ret[0] {}".format(ret[0]))
        if ret[0] == 200:
            xraylist = ret[1]
            print("getAllXRays for patient {} clinic {} {}".format(patientid,
clinicid, xraylist))
            for x in xraylist:
                y = GetImage(sess.getHost(), sess.getPort(), sess.getToken())
                y.setId(x)
                ret = y.send(timeout=30)
                if ret[0] == 200:
                    xrays.append(ret[1])
        return xrays

    def uploadXRay(self, sess, imagegrid, clinicid, patientid, path):
        x = CreateImage(sess.getHost(), sess.getPort(), sess.getToken())
        x.setClinic(clinicid)
        x.setPatient(patientid)
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        x.setData(str(encoded_string, 'utf-8'))
        x.setType("Xray")
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("uploadXRay success id is {}".format(ret[1]["id"]))
            imagegrid.toggleDeleteButtonState()
            return ret[1]["id"]
        else:
            print("uploadXRay failed ret[0] {}".format(ret[0]))

    def removeXRay(self, sess, imagegrid, id):
        ret = False
        x = DeleteImage(sess.getHost(), sess.getPort(), sess.getToken(), id)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            ret = True
            print("deleted XRay image {}".format(id))
        else:
            print("XRay failed to delete XRay image {}".format(id))
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
                    p["dob"] = self.orderByYearMonthDay(y["dob"])
                    p["gender"] = y["gender"]
                    patients.append(p)
        return patients

    def orderByYearMonthDay(self, dob):
        y = dob.split("/")
        return "{}/{}/{}".format(y[2], y[0], y[1]) 

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
                        p["dob"] = self.orderByYearMonthDay(y["dob"])
                        p["gender"] = y["gender"]
                        patients.append(p)
        return patients

def usage():
    print("tsdashboard [-h host] [-p port] -u username -w password") 

class XRayTab(wx.Panel):

    def getTitle(self):
        return "X-Ray Uploader"

    def on_upload(self, event):
        filepath = self.photo_ctrl.get_image_path()
        xrays = XRays()
        print("calling uploadXRay sess {} imagegrid {} clinic {} patient {} filepath {}".format(self.sess, self.imagegrid, self.main.clinic,
self.main.patient, filepath))
        ret = xrays.uploadXRay(self.sess, self.imagegrid, self.main.clinic,
self.main.patient, filepath)
        if not ret == None:
            self.imagegrid.add(filepath, id=ret)
            pub.sendMessage('disableupload')
            pub.sendMessage("clearxraycontrol")
            pub.sendMessage('refresh')

    def on_delete(self, event):
        dlg = wx.MessageDialog(None, "Are you sure you want to delete the selected XRay(s)? This operation cannot be undone.",'Confirm Delete',wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()

        if result == wx.ID_YES:
            print( "Yes pressed")
        else:
            print( "No pressed")
            return

        deleteList = self.imagegrid.getDeleteList()
        cleanup = []
        if deleteList:
            xrays = XRays()
            for x in deleteList:
                ret = xrays.removeXRay(self.sess, self.imagegrid, x)
                if ret == True:
                    cleanup.append(x)
            for x in cleanup:
                self.imagegrid.removeFromDeleteList(x)
            pub.sendMessage('clearxrays')
            pub.sendMessage('loadxrays')

    def on_load_xrays(self):
        xrays = XRays()
        patientXrays = xrays.getAllXRays(self.sess, self.main.clinic,
self.main.patient)
        for x in patientXrays:
            fp = tempfile.NamedTemporaryFile(delete=False)
            tmp_name = fp.name
            fp.write(base64.b64decode(x['data']))
            fp.close() # on Windows, need to close before adding to grid
            self.imagegrid.add(fp.name, x["id"])
            os.unlink(tmp_name)

    def on_disable_upload_message(self):
        self.upload_btn.Disable()

    def on_enable_upload_message(self):
        self.upload_btn.Enable()

    def disable_delete(self):
        self.delete_btn.Disable()

    def enable_delete(self):
        self.delete_btn.Enable()

    def __init__(self, parent, main, sess):
        self.sess = sess
        self.main = main
        wx.Panel.__init__(self, parent)

        image_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.photo_ctrl = PhotoCtrl(parent=self, sess=self.sess)

        image_sizer.Add(self.photo_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.upload_btn = wx.Button(self, label='Upload X-Ray')
        self.upload_btn.Disable()
        self.upload_btn.Bind(wx.EVT_BUTTON, self.on_upload)
        image_sizer.Add(self.upload_btn, 0, wx.LEFT, 5)

        self.delete_btn = wx.Button(self, label='Delete Selected')
        self.delete_btn.Disable()
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        image_sizer.Add(self.delete_btn, 0, wx.LEFT, 5)

        isizer = wx.BoxSizer(wx.VERTICAL)
        txt = 'X-Rays Uploaded for This Patient and Clinic'
        label = wx.StaticText(self, label=txt)
        isizer.Add(label, 0, wx.ALL | wx.CENTER, 5)

        self.imagegrid = ImageGrid(parent=self)
        isizer.Add(self.imagegrid, 1, wx.ALL | wx.EXPAND, 5)
        image_sizer.Add(isizer, 1, wx.ALL | wx.EXPAND)
        pub.subscribe(self.on_load_xrays, 'loadxrays')
        pub.subscribe(self.on_disable_upload_message, 'disableupload')
        pub.subscribe(self.on_enable_upload_message, 'enableupload')
        pub.subscribe(self.disable_delete, 'disable_delete')
        pub.subscribe(self.enable_delete, 'enable_delete')
        self.SetSizer(image_sizer)

class PrintWristBandTab(wx.Panel):
    def getTitle(self):
        return "Wrist Band Printer"

    def dobToMilitary(self, dob):
        try :
            parts = dob.split('/')
            months = [
                  "JAN",
                  "FEB",
                  "MAR",
                  "ABR",
                  "MAY",
                  "JUN",
                  "JUL",
                  "AGO",
                  "SEP",
                  "OCT",
                  "NOV",
                  "DIC",
                 ]
            return "{}{}{}".format(parts[2], months[int(parts[1]) - 1], parts[0])
        except:
            return dob

    def updatePrintStr(self):

        val = "{} {} {} {} {} {} {}".format(
            str(self.patientData.id) if self.idcb.GetValue() else "",
            self.first.GetValue() if self.firstcb.GetValue() else "",
            self.middle.GetValue() if self.middlecb.GetValue() else "",
            self.father.GetValue().upper() if self.fathercb.GetValue() else "",
            self.mother.GetValue().upper() if self.mothercb.GetValue() else "",
            self.dobToMilitary(self.dob.GetValue()) if self.dobcb.GetValue() else "",
            self.gender.GetValue() if self.gendercb.GetValue() else "")
            
        self.labelText.SetLabel(val)

    def on_patient_selected_message(self, data, patient):
        self.patientData = data

        print("wristband printer on_patient_selected {}".format(data))

        self.id.SetValue(str(data.id))
        self.first.SetValue(data.first)
        self.middle.SetValue(data.middle)
        self.father.SetValue(data.paternal_last)
        self.mother.SetValue(data.maternal_last)
        self.dob.SetValue(data.dob)
        self.gender.SetValue(data.gender)
        #self.curp.SetText(data.gender)

        self.updatePrintStr()

        '''
        self.first = data['first']
        self.middle = data['middle']
        self.paternal_last = data['paternal_last']
        self.maternal_last = data['maternal_last']
        self.dob = data['dob']
        self.gender = data['gender']
        self.curp = data['curp']
        '''

        print("on_patient_selected_message {}".format(patient))
        self.patient = patient

    def onChecked(self, e):
        self.updatePrintStr()

    def onEnter(self, e):
        self.updatePrintStr()

    def __init__(self, parent, main, sess):
        self.sess = sess
        self.main = main
        wx.Panel.__init__(self, parent)

        pub.subscribe(self.on_patient_selected_message, 'patient_selected')

        container = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # id 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="ID")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.id = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        self.Bind(wx.EVT_TEXT, self.onEnter)
        vsizer.Add(self.id, 0, wx.ALL, 5)
        self.idcb = wx.CheckBox(self, label="")
        self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
        vsizer.Add(self.idcb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        # first 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="First")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.first = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.first, 0, wx.ALL, 5)
        self.firstcb = wx.CheckBox(self, label="")
        self.firstcb.SetValue(True)
        vsizer.Add(self.firstcb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        # middle 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="Middle")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.middle = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.middle, 0, wx.ALL, 5)
        self.middlecb = wx.CheckBox(self, label="")
        self.middlecb.SetValue(True)
        vsizer.Add(self.middlecb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        # father 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="Father's Last")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.father = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.father, 0, wx.ALL, 5)
        self.fathercb = wx.CheckBox(self, label="")
        self.fathercb.SetValue(True)
        vsizer.Add(self.fathercb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        # mother 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="Mather's Last")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.mother = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.mother, 0, wx.ALL, 5)
        self.mothercb = wx.CheckBox(self, label="")
        self.mothercb.SetValue(True)
        vsizer.Add(self.mothercb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        container.Add(hsizer, 0, wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # gender 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="Gender")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.gender = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.gender, 0, wx.ALL, 5)
        self.gendercb = wx.CheckBox(self, label="")
        self.gendercb.SetValue(True)
        vsizer.Add(self.gendercb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        # dob 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="DOB")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.dob = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.dob, 0, wx.ALL, 5)
        self.dobcb = wx.CheckBox(self, label="")
        self.dobcb.SetValue(True)
        vsizer.Add(self.dobcb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)

        '''
        # curp 
        vsizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self,
                            label="CURP")
        vsizer.Add(lbl, 0, wx.ALL, 5)
        self.curp = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(200, 30))
        #self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        vsizer.Add(self.curp, 0, wx.ALL, 5)
        self.curpcb = wx.CheckBox(self, label="")
        vsizer.Add(self.curpcb, 0, wx.ALL, 5)
        hsizer.Add(vsizer, 0, wx.ALL, 5)
        '''

        container.Add(hsizer, 0, wx.ALL, 5)

        self.labelText = wx.StaticText(self,-1,style = wx.ALIGN_LEFT) 
        font = wx.Font(24, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        self.labelText.SetFont(font)
        self.labelText.SetLabel("ipso facto absurdum")
        container.Add(self.labelText, 0, wx.ALL, 5)

        self.print_btn = wx.Button(self, label='Print')
        #self.print_btn.Bind(wx.EVT_BUTTON, self.on_print)
        container.Add(self.print_btn, 0, wx.ALL, 5)

        self.SetSizer(container)

class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the third tab", (20,20))

class TabFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the last tab", (20,20))

class TabPanel(wx.Notebook):
    def __init__(self, parent, sess):
        super().__init__(parent)

        # Create the tab windows
        tab1 = XRayTab(self, parent, sess)
        tab2 = PrintWristBandTab(self, parent, sess)

        # Add the windows to tabs and name them.
        self.AddPage(tab1, tab1.getTitle())
        self.AddPage(tab2, tab2.getTitle())

class MainPanel(wx.Panel):

    def __init__(self, parent, sess, clinics):
        super().__init__(parent)
        self.sess = sess
        self.patient = None
        self.search_term = None

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
        self.clinics = wx.ListCtrl(self, style=wx.LC_REPORT)
        #self.clinics = wx.ListCtrl(self, size=(-1, -1), style=wx.LC_REPORT)
        
        self.clinics.InsertColumn(0, "Clinic Number")
        self.clinics.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.clinics.InsertColumn(1, "Location")
        self.clinics.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.clinics.InsertColumn(2, "Start Date")
        self.clinics.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.clinics.InsertColumn(3, "End Date")
        self.clinics.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)

        index = 0
        for i in clinics: 
            self.clinics.InsertStringItem(index, str(i["id"])) 
            self.clinics.SetStringItem(index, 1, i["location"]) 
            self.clinics.SetStringItem(index, 2, i["start"])
            self.clinics.SetStringItem(index, 3, i["end"])
            index += 1

        self.clinics.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_clinic, self.clinics)
        clinics_sizer.Add(self.clinics, 1, wx.ALL| wx.EXPAND)
        self.search = wx.SearchCtrl(
            self, style=wx.TE_PROCESS_ENTER, size=(-1, 25))
        self.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.on_search)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        search_sizer.Add(self.search, 1, wx.EXPAND)
        
        self.main_sizer.Add(clinics_sizer, 1, wx.ALL|wx.EXPAND, 5)
        self.main_sizer.Add(search_sizer, 0, wx.ALL |wx.EXPAND)

        self.search_panel = RegularSearch(self, sess)
        self.main_sizer.Add(self.search_panel, 1, wx.ALL | wx.EXPAND)

        self.tabPanel = TabPanel(self, sess)
        self.main_sizer.Add(self.tabPanel, 1, wx.ALL | wx.EXPAND)
        self.tabPanel.Show()

        pub.subscribe(self.on_patient_selected_message, 'patient_selected')
        pub.subscribe(self.on_refresh_message, 'refresh')
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timerHandler, self.timer)
        self.timer.Start(60000)
        self.SetSizer(self.main_sizer)

    def timerHandler(self, event):
        print("updated: {}".format(time.ctime()))
        self.on_search(None)
        pub.sendMessage('patients_updated')

    def on_refresh_message(self):
        print("on_refresh_message")
        self.Layout()

    def on_patient_selected_message(self, data, patient):
        print("on_patient_selected_message {}".format(patient))
        self.patient = patient
        self.patientData = data

    def setClinic(self, id):
        self.clinic = id

    def set_registrations(self, registrations):
        self.search_panel.load_search_results(registrations)

    def on_clinic(self, event):
        pub.sendMessage("clearxrays")
        pub.sendMessage("pulseon")
        ind = event.GetIndex()
        item = self.clinics.GetItem(ind, 0)
        regs = Registrations()
        self.clinic = int(item.GetText())
        patientsThisClinic = regs.getAllRegistrations(self.sess, self.clinic)
        self.set_registrations(patientsThisClinic)
        if len(patientsThisClinic):
            self.search_panel.update_image(int(patientsThisClinic[0]["id"]))
        pub.sendMessage("pulseoff")

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

class SearchFrame(wx.Frame):

    def __init__(self, sess, clinics):
        super().__init__(None, title='Thousand Smiles Clinic Dashboard',
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
