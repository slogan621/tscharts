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

import wx
from pubsub import pub

class ImageGrid(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent 
        sizer = wx.BoxSizer(wx.VERTICAL)
        txt = 'X-Rays Uploaded for This Patient and Clinic'
        label = wx.StaticText(self, label=txt)
        sizer.Add(label, 1, wx.ALL | wx.CENTER, 5)
       
        self.grid = wx.GridSizer(5, 5, 5, 5)
        self.SetBackgroundColour('light blue') 
        self.SetMinSize(wx.Size(400, 300))
        sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.Layout()
        self.Show()
        pub.subscribe(self.on_clear_message, 'clearxrays')      

    def add(self, path):
        photoMaxSize = 60
        img = wx.Image(photoMaxSize, photoMaxSize)
        imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = photoMaxSize
            NewH = photoMaxSize * H / W
        else:
            NewH = photoMaxSize
            NewW = photoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        imageCtrl.SetBitmap(wx.Bitmap(img))
        self.grid.Add(imageCtrl)
        self.grid.ShowItems(True)
        pub.sendMessage("refresh")

    def on_clear_message(self):
        self.grid.ShowItems(False)
        self.clear();
        self.Layout()
        pub.sendMessage("refresh")
 
    def clear(self):
        try:
            self.grid.Clear()
        except:
            pass
