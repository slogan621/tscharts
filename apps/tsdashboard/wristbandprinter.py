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


# Notes:
# Printing from the raspberry pi uses the CUPS driver solution.
# General Info on the Zebra ZD510-HC can be found at:
# https://www.zebra.com/us/en/support-downloads/printers/desktop/zd510-hc.html
# There is a specific link for information on the CUPS package.
#
# Once installed, the driver needs to be configured for this printer:
# Size: custom
# Width = 1
# Heigth = 7.024 (May need to change for different sizes.
# Units: Inches
# Resolution: 300dpi
# Meadia Tracking: Non-continuous (Mark sensing)
# Mesia Type: Printer default
#
# In my .bashrc file, I also set this:
# export PRINTER="Zebra_Technologies_ZTC_ZD510-300dpi_ZPL"
#
# The application uses LPR, so this export is required.



class WristBandPrinter:
    def __init__(self):
        pass

    def getUserFormattedWristband(self):
        return self.__str__();

# Because the second line cut off the first few characters,
# place six spaces after the "\n" on the beginning of the second line.

    def __str__(self):
        val = "{}{} {}{} {}{} {}{} {}{} {}{} {}{} {}".format(
        str(self._patientData.id) if self._idShow else "",
        "\n      " if self._idnl else "",
        self._patientData.first if self._firstShow else "",
        "\n      " if self._firstnl else "",
        self._patientData.middle if self._middleShow else "",
        "\n      " if self._middlenl else "",
        self._patientData.father.upper() if self._fatherShow else "",
        "\n      " if self._fathernl else "",
        self._patientData.mother if self._motherShow else "",
        "\n      " if self._mothernl else "",
        self._patientData.gender if self._genderShow else "",
        "\n      " if self._gendernl else "",
        self._patientData.dob if self._dobShow else "",
        "\n      " if self._dobnl else "",
        self._patientData.curp if self._curpShow else "")

        return val

    def setPatientData(self, data):
        self._patientData = data

    def setNewlineFlags(self, id, first, middle, father, mother, dob, gender,
curp):
        self._idnl = id
        self._firstnl = first
        self._middlenl = middle
        self._fathernl = father
        self._mothernl = mother
        self._dobnl = dob
        self._gendernl = gender
        self._curpnl = curp

    def setShowFlags(self, id, first, middle, father, mother, dob, gender,
curp):
        self._idShow = id
        self._firstShow = first
        self._middleShow = middle
        self._fatherShow = father
        self._motherShow = mother
        self._dobShow = dob
        self._genderShow = gender
        self._curpShow = curp

#
# This procedure actually sends the ASCII data to the printer using lpr.
# First open a temporary file in /tmp
# Then send a newline and six spaces to the file.
# Without the spaces, the patient ID is cut off.
# Then send the wristband string to the file
# Close the file.
# The original print to the screen is still present.
# Then, using the command lpr, print the file to the zebra printer
#
# Asumption: The same filename is used each time. The asumption is that lpr will
# read in the file before another one is created. The printing is very fast, so
# hopefully this will work. Otherwise, a temporary filename will be needed, and
# cleanup will have to be done. This way no cleanup is needed.
#
    def sendToPrinter(self):
        import sys
        import os

        wristbandStr = self.getUserFormattedWristband()
        
        f= open("/tmp/test.txt","w+")
        f.write("\n      ")
        f.write(wristbandStr)
        f.close()
        print("{}".format(wristbandStr))
        os.system("lpr -o orientation-requested=4 /tmp/test.txt")


def main():

    # example code as called by UI

    printer = WristBandPrinter()

    patientData = lambda: None
    patientData.id = 1234
    patientData.first = "firstname"
    patientData.middle = "middlename"
    patientData.father = "father"
    patientData.mother = "mother"
    patientData.dob = "23OCT2014"
    patientData.gender = "female"
    patientData.curp = "123456789abcdef"

    printer.setPatientData(patientData)
    printer.setShowFlags(id=True, first=True, middle=True, father=True, mother=True, dob=True, gender=True, curp=True)
    printer.setNewlineFlags(id=False, first=False, middle=False, father=False, mother=True, dob=False, gender=False, curp=False)
    printer.sendToPrinter()

if __name__ == "__main__":
    main()
