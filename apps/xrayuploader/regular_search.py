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

import os
import tempfile
import base64
import requests
import wx

from download_dialog import DownloadDialog
from ObjectListView import ObjectListView, ColumnDefn
from pubsub import pub
from urllib.parse import urlencode, quote_plus
from test.image.image import GetImage

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
            #pub.sendMessage('refresh')
        self.timer_update = False

    def on_selection(self, event):
        selection = self.search_results_olv.GetSelectedObject()
        print("selected object {}".format(selection))
        #patient_id = self.title.SetValue(f'{selection.id}')
        #self.title.SetValue(f'{selection.title}')
        self.selected_id = selection.id
        self.update_image(f'{selection.id}')
        if not self.timer_update:
            pub.sendMessage('clearxrays')
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
            ColumnDefn("Paternal Last", "left", 250, "paternal_last"),
            ColumnDefn("Maternal Last", "left", 350, "maternal_last"),
            ColumnDefn("First", "left", 100, "first"),
            ColumnDefn("Middle", "left", 150, "middle"),
            ColumnDefn("Date of Birth", "left", 150, "dob"),
            ColumnDefn("Gender", "left", 150, "gender"),
        ])
        self.search_results_olv.SetObjects(self.search_results)

    def load_search_results(self, registrations):
        self.search_results = []
        for item in registrations:
            result = Result(item)
            self.search_results.append(result)
        self.update_search_results()
