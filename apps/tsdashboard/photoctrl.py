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
import wx
from PIL import Image
from pubsub import pub

PhotoMaxSize = 240

class DropTarget(wx.FileDropTarget):
    
    def __init__(self, widget):
        wx.FileDropTarget.__init__(self)
        self.widget = widget
        
    def OnDropFiles(self, x, y, filenames):
        image = Image.open(filenames[0])
        image.thumbnail((PhotoMaxSize, PhotoMaxSize))
        image.save('thumbnail.png')
        pub.sendMessage('dnd', filepath='thumbnail.png')
        return True
        
class PhotoCtrl(wx.Panel):
    def __init__(self, parent, sess, redirect=False, filename=None):
        super().__init__(parent)
        #self.frame = wx.Frame(None, title='Photo Control')
        #self.panel = wx.Panel(self.frame)
        #self.panel = wx.Panel(parent)
        pub.subscribe(self.update_image_on_dnd, 'dnd')
        self.createWidgets()
        #self.frame.Show()
        self.filename = filename;
        pub.subscribe(self.on_clearxraycontrol_message, 'clearxraycontrol')

    def on_clearxraycontrol_message(self):
        img = wx.Image(240,240)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.photoTxt.SetValue("")
        self.Layout()
        pub.sendMessage("refresh")

    def createWidgets(self):
        instructions = 'Browse for an image or Drag and Drop'
        img = wx.Image(240,240)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
                                         wx.Bitmap(img))
        filedroptarget = DropTarget(self)
        self.imageCtrl.SetDropTarget(filedroptarget)
        #instructLbl = wx.StaticText(self, label=instructions)
        self.photoTxt = wx.TextCtrl(self, size=(200,-1))
        browseBtn = wx.Button(self, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_browse)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        #self.panel.SetSizer(self.mainSizer)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
        self.Layout()
        self.Show()

    def on_browse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg| PNG Files (*.png)|*.png"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.on_view()

    def get_image_path(self):
        return self.filename
        
    def update_image_on_dnd(self, filepath):
        self.on_view(filepath=filepath)

    def on_view(self, filepath=None):
        if not filepath:
            filepath = self.photoTxt.GetValue()
        self.filename = filepath
            
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = PhotoMaxSize
            NewH = PhotoMaxSize * H / W
        else:
            NewH = PhotoMaxSize
            NewW = PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        pub.sendMessage('enableupload')
        self.Refresh()
