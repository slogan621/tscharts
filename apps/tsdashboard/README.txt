Dependencies
------------

wxPython
Python 3 only

Notes
-----

Rename tscharts/queue, which conflicts with python 3 urllib. May rename
queue to something else (maybe schedqueue) in the future.

Creating a binary for Windows
-----------------------------

Visit pyinstaller.org

On the main page, find PyInstaller Quickstart, and follow the directions.
In summary (this can be done within a git clone of the repo and on a
Linux host):

$ cd tsdashboard
$ pyinstaller tsdashboard.py

Make a zip file of the resulting dist/tsdashboard directory and unpack on
the target Windows 10 machine. Example zip creation on linux:

$ zip -r tsdashboardv1.1.zip dist/tsdashboard

Finally, create a shortcut for the desktop:
https://drive.google.com/drive/u/0/folders/1x9BHnvAm53Yq2QCbPqdBsMELS1oSaNNa
for detailed instructions.

