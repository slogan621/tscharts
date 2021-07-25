#(C) Copyright Syd Logan 2020-2021
#(C) Copyright Thousand Smiles Foundation 2020-2021
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

import os
import tempfile
import base64
import requests
import wx

from download_dialog import DownloadDialog
from ObjectListView import ObjectListView, ColumnDefn
from pubsub import pub
from urllib.parse import urlencode, quote_plus
from tschartslib.image.image import GetImage
import wx.lib.agw.pyprogress as PP

class Headshot():
    def getHeadshot(self, sess, patient):
        tmp_location = None
        image = GetImage(sess.getHost(), sess.getPort(), sess.getToken())
        image.setPatient(patient)
        image.setType("Headshot")
        image.setNewest("true")
        ret = image.send(timeout=30)
        if ret[0] == 200: 
            filename = "patient_headshot_{}".format(patient)
            tmp_location = "{}_{}".format(tempfile.TemporaryDirectory().name, filename)
            data = base64.standard_b64decode(ret[1]["data"])
            f = open(tmp_location, 'wb+')
            f.write(data)
            f.close()
        return tmp_location 

class Result:

    def __init__(self, data):
        self.id = data['id']
        self.first = data['first']
        self.middle = data['middle']
        self.paternal_last = data['paternal_last']
        self.maternal_last = data['maternal_last']
        self.dob = data['dob']
        self.gender = data['gender']
        self.curp = data['curp']

class RegularSearch(wx.Panel):

    def __init__(self, parent, sess):
        super().__init__(parent)
        self.sess = sess
        self.selected_id = None
        self.timer_update = False
        self.search_results = []
        self.max_size = 300
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        pub.subscribe(self.on_pulse_on_message, "pulseon")
        pub.subscribe(self.on_pulse_off_message, "pulseoff")
        sub_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.paths = wx.StandardPaths.Get()
        pub.subscribe(self.load_search_results, 'search_results')
        pub.subscribe(self.on_patients_updated, 'patients_updated')

        self.search_results_olv = ObjectListView(
            self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.search_results_olv.SetEmptyListMsg("No Results Found")
        self.search_results_olv.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                     self.on_selection)
        sub_sizer1.Add(self.search_results_olv, 1, wx.EXPAND)
        self.update_search_results()

        '''
        main_sizer.AddSpacer(30)
        self.title = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.title.SetFont(font)
        main_sizer.Add(self.title, 0, wx.ALL|wx.EXPAND, 5)
        '''
        img = wx.Image(240, 240)
        self.image_ctrl = wx.StaticBitmap(self,
                          bitmap=wx.Bitmap(img))
        sub_sizer1.Add(self.image_ctrl, 0, wx.LEFT|wx.ALL, 5)

        self.SetSizer(main_sizer)
        main_sizer.Add(sub_sizer1, 0, wx.ALL, 5)
        main_sizer.Add(sub_sizer, 1, wx.ALL, 5)

    def on_patients_updated(self):
        self.timer_update = True
        self.on_pulse_on_message()
        if self.selected_id:
            objs = self.search_results_olv.GetObjects()
            count = 0
            for x in objs:
                if x.id == self.selected_id:
                    self.search_results_olv.SelectObject(x)
                    self.search_results_olv.EnsureCellVisible(count, 0)
                    break
                count = count + 1
            self.update_image(f'{self.selected_id}')
        else: 
            try:
                selection = self.search_results_olv.GetSelectedObject()
            except:
                selection = None

            try:
                if selection == None:
                    obj = self.search_results_olv.GetObjectAt(0);
                    if obj != None:
                        self.search_results_olv.SelectObject(obj)
                        self.selected_id = obj.id 
                        pub.sendMessage('patient_selected', data=obj, patient=self.selected_id)
            except:
                pass
           

        self.on_pulse_off_message()
        self.timer_update = False

    # XXX this doesn't work as it should, likely because of
    # wx main loop processing. Revisit

    def pulseTimerHandler(self, event):
        #self.gauge.Pulse()
        #self.dlg.UpdatePulse()
        self.dlg.Pulse()

    def on_pulse_on_message(self):
        #self.gauge.Show()
        self.pulsetimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.pulseTimerHandler, self.pulsetimer)
        style = wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME
        #self.dlg = PP.PyProgress(self, -1, "PyProgress Example",
        #                    "An Informative Message", agwStyle=style)
        self.dlg = wx.ProgressDialog("Clinic Loading", "Please Wait", 100,
                            style=style)
        self.pulsetimer.Start(500)

    def on_pulse_off_message(self):
        self.pulsetimer.Stop()
        #self.gauge.Hide()
        self.dlg.Destroy()

    def on_selection(self, event):
        selection = self.search_results_olv.GetSelectedObject()
        #patient_id = self.title.SetValue(f'{selection.id}')
        #self.title.SetValue(f'{selection.title}')
        if selection and selection.id:
            self.selected_id = selection.id
            self.update_image(f'{selection.id}')
            if not self.timer_update:
                pub.sendMessage('clearxrays')
                pub.sendMessage('clearxraycontrol')
                pub.sendMessage('patient_selected', data=selection, patient=self.selected_id)
                pub.sendMessage('loadxrays')
        '''
        else:
            img = wx.Image(240, 240)
            self.image_ctrl.SetBitmap(wx.Bitmap(img))
            self.Refresh()
            self.Layout()
        '''

    def update_image(self, patient_id):
        headshot = Headshot()
        tmp_location = headshot.getHeadshot(self.sess, patient_id)
        if not tmp_location:
            img = wx.Image(240, 240)
        else:
            if os.path.exists(tmp_location):
                img = wx.Image(tmp_location, wx.BITMAP_TYPE_ANY)
                '''
                W = img.GetWidth()
                H = img.GetHeight()
                if W > H:
                    NewW = self.max_size
                    NewH = self.max_size * H / W
                else:
                    NewH = self.max_size
                    NewW = self.max_size * W / H
                img = img.Scale(NewW,NewH)
                '''
                img = img.Scale(240,240)

        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()
        self.Layout()

    '''
    def update_image(self, url):
        filename = url.split('/')[-1]
        tmp_location = os.path.join(self.paths.GetTempDir(), filename)
        r = requests.get(url)
        with open(tmp_location, "wb") as thumbnail:
            thumbnail.write(r.content)

        if os.path.exists(tmp_location):
            img = wx.Image(tmp_location, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H = img.GetHeight()
            if W > H:
                NewW = self.max_size
                NewH = self.max_size * H / W
            else:
                NewH = self.max_size
                NewW = self.max_size * W / H
            img = img.Scale(NewW,NewH)
        else:
            img = wx.Image(240, 240)

        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()
        self.Layout()
    '''

    def reset_image(self):
        img = wx.Image(240, 240)
        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()

    def update_search_results(self):
        self.search_results_olv.SetColumns([
            ColumnDefn("ID", "left", 250, "id"),
            ColumnDefn("CURP", "left", 150, "curp"),
            ColumnDefn("Paternal Last", "left", 250, "paternal_last"),
            ColumnDefn("Maternal Last", "left", 350, "maternal_last"),
            ColumnDefn("First", "left", 100, "first"),
            ColumnDefn("Middle", "left", 150, "middle"),
            ColumnDefn("Date of Birth", "left", 150, "dob"),
            ColumnDefn("Gender", "left", 150, "gender"),
        ])
        if len(self.search_results):
            self.search_results_olv.SetObjects(self.search_results)
            pub.sendMessage('patients_updated')

    def load_search_results(self, registrations):
        self.search_results = []
        for item in registrations:
            result = Result(item)
            self.search_results.append(result)
        self.update_search_results()
