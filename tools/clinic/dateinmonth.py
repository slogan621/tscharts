#(C) Copyright Syd Logan 2022
#(C) Copyright Thousand Smiles Foundation 2022
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

import datetime

'''
Get the date corresponding to the nth occurance of a given day in a month 
for a specific year. 

@param[in] year year the month occurs in
@param[in] month month value 1=Jan, 12=Dec
@param[in] n occurance of day we want to find, 1 = first, 2 = second, etc.
@param[in] aday the day we are interested in (1 = sunday, 7 = saturday)

@note python datetime iso considers 1 to be monday, so we need to convert

@return a date object if the parameters are valid, otherwise None
'''

def GetNthDateInMonth(year, month, n, aday):

    # get object representing first day of month

    dayval = 1
    day = datetime.date(year, month, dayval)

    # figure out what day (sunday, monday, etc.) the month starts on

    dayofweek = day.isoweekday()

    # map from our Sunday = 1 to python Monday = 1

    aday += 6
    if aday > 7:
        aday -= 7
    
    # get number of days in this month by trying to get last day starting
    # with 31 until we don't trigger an exception. hacky, but effective.

    tries = (31, 30, 29, 28)
    thismonthlen = -1

    for monthlen in tries:
        try:
            foo = datetime.date(year, month, monthlen)
            thismonthlen = monthlen
            break
        except:
            pass

    # month doesn't have 28 - 31 days? impossible, but return None
    # in case this happens (probably should throw an exception of
    # some kind.)
   
    if thismonthlen == -1:
        print "Couldn't determine length of month"
        return None

    # find day number of first occurance of the day (monday, etc..) in the
    # month

    while dayofweek != aday and dayval < thismonthlen:
        dayofweek += 1
        dayval += 1
        if dayofweek > 7:
            dayofweek = 1

    # get the day number of the nth occurance of this day

    n -= 1
    dayval += (7 * n)

    # such a day does not exist, so return None

    if dayval > thismonthlen:
        print "dayval ", dayval, " > thismonthlen ", thismonthlen
        return None

    day = datetime.date(year, month, dayval)
    return day

def main():
    adate = GetNthDateInMonth(2022, 2, 1, 6)
    print adate
    adate = GetNthDateInMonth(2013, 8, 1, 6)
    print adate
    

if __name__ == "__main__":
    main()
