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

class WristBandPrinter:
    def __init__(self):
        pass

    def getUserFormattedWristband(self):
        return self.__str__();
        
    def __str__(self):
        val = "{}{} {}{} {}{} {}{} {}{} {}{} {}{} {}".format(
        str(self._patientData.id) if self._idShow else "",
        "\n" if self._idnl else "",
        self._patientData.first if self._firstShow else "",
        "\n" if self._firstnl else "",
        self._patientData.middle if self._middleShow else "",
        "\n" if self._middlenl else "",
        self._patientData.father.upper() if self._fatherShow else "",
        "\n" if self._fathernl else "",
        self._patientData.mother if self._motherShow else "",
        "\n" if self._mothernl else "",
        self._patientData.gender if self._genderShow else "",
        "\n" if self._gendernl else "",
        self._patientData.dob if self._dobShow else "",
        "\n" if self._dobnl else "",
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

    def sendToPrinter(self):
        wristbandStr = self.getUserFormattedWristband()
        print("{}".format(wristbandStr))

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
