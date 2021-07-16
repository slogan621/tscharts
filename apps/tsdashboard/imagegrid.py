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
import wx.lib.scrolledpanel as scrolled

# https://wiki.wxpython.org/ScrolledWindows

class ImageGrid(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent 
        ##sizer = wx.BoxSizer(wx.VERTICAL)
        #txt = 'X-Rays Uploaded for This Patient and Clinic'
        #label = wx.StaticText(self, label=txt)
        #sizer.Add(label, 1, wx.ALL | wx.CENTER, 5)

        self.grid = wx.FlexGridSizer(cols=6, hgap=5, vgap=5)   # rows, cols, hgap, vgap 
        self.SetBackgroundColour('light blue') 
        self.SetSizer(self.grid)
        self.Layout()
        self.Show()
        pub.subscribe(self.on_clear_message, 'clearxrays')
        self.deleteList = []

    def getDeleteList(self):
        return self.deleteList;

    def addToDeleteList(self, id):
        self.deleteList.append(id)
        self.toggleDeleteButtonState() 

    def removeFromDeleteList(self, id):
        self.deleteList.remove(id)
        self.toggleDeleteButtonState() 

    def toggleDeleteButtonState(self):
        if self.getDeleteListSize() == 0:
            pub.sendMessage("disable_delete")
        else:
            pub.sendMessage("enable_delete")
   
    def getDeleteListSize(self):
        return len(self.deleteList)

    def add(self, path, id):
        photoMaxSize = 60
        sizer = wx.BoxSizer(wx.VERTICAL)
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
        checkBox = wx.CheckBox(self, label = 'Delete', pos = (10,10)) 

        def onChecked(self, e, args): 
            imageId = args[0]
            deleteList = args[1]
            checkBox = args[2]
            '''
            print("onChecked: id is {} e is {} value {}".format(imageId, e,
checkBox.GetValue()))
            '''
            if checkBox.GetValue() == True:
                self.addToDeleteList(imageId)
            else:
                try:
                    self.removeFromDeleteList(imageId)
                except:
                    pass

            if self.getDeleteListSize() == 0:
                pub.sendMessage("disable_delete")
            else:
                pub.sendMessage("enable_delete")
   
        checkBox.Bind(wx.EVT_CHECKBOX, lambda event: onChecked(self=self, e=event, args=(id,
self.deleteList, checkBox)))
        sizer.Add(imageCtrl, 1, wx.ALL | wx.CENTER, 5)
        sizer.Add(checkBox, 1, wx.ALL | wx.CENTER, 5)
        self.grid.Add(sizer, flag=wx.ALL | wx.EXPAND, border=5)
        self.grid.ShowItems(True)
        pub.sendMessage("refresh")

        self.SetupScrolling();

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
