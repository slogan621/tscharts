**Get ENT Treatment**

----
  Returns json data about a single ENT treatment resource. 

* **URL**

  /tscharts/v1/enttreatment/id

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

  Response is a JSON object with the following fields:

  "id" : id,<br />
  "clinic" : id, <br />
  "patient" : id, <br />
  "time" : UTC date time string, <br />
  "earCleanedSide" : "both" | "left" | "right" | "none",<br />
  "earCleanedComment" : text<br />
  "audiogramSide" : "both" | "left" | "right" | "none", <br />
  "audiogramComment" : text,<br />
  "audiogramRightAway" : true | false<br />
  "audiogramRightAwayComment" : text,<br />
  "tympanogramSide" : "both" | "left" | "right" | "none",<br />
  "tympanogramComment" : text,<br />
  "tympanogramRightAway" : true | false, <br />
  "tympanogramRightAwayComment" : text,<br />
  "mastoidDebridedSide" : "both" | "left" | "right" | "none",<br />
  "mastoidDebridedComment" : text,<br />
  "mastoidDebridedHearingAidEval" : true | false,<br />
  "mastoidDebridedHearingAidEvalComment" : text,<br />
  "antibioticDrops" : true | false <br />
  "antibioticDropsComment" : text,<br />
  "antibioticOrally" : true | false <br />
  "antibioticOrallyComment" : text,<br />
  "antibioticAcuteInfection" : true | false,<br />
  "antibioticAcuteInfectionComment" : text,<br />
  "antibioticAfterWaterExposureInfectionPrevention" : true | false,<br />
  "antibioticAfterWaterExposureInfectionPreventionComment" : text,<br />
  "boricAcidToday" : true | false<br />
  "boricAcidTodayComment" : text,<br />
  "boricAcidForHomeUse" : true | false, <br />
  "boricAcidForHomeUseComment" : text,<br />
  "boricAcidSide" : "both" | "left" | "right" | "none",<br />
  "boricAcidSideComment" : text,<br />
  "foreignBodyRemoved" : <br />
  "foreignBodyRemovedComment" : text,<br />
  "return3Months" : true | false <br />
  "return6Months" : true | false, <br />
  "returnPrn" : true | false <br />
  "returnComment" : text,<br />
  "referredPvtENTEnsenada" : true | false <br />
  "referredPvtENTEnsenadaComment" : text,<br />
  "referredChildrensHospitalTJ" : true | false,<br />
  "referredChildrensHospitalTJComment" : text,<br />
<br />
  "tubesTomorrow" : "both" | "left" | "right" | "none",<br />
  "tubesTomorrowComment" : text,<br />
  "tPlastyTomorrow" : "both" | "left" | "right" | "none",<br />
  "tPlastyTomorrowComment" : text,<br />
  "euaTomorrow" : "both" | "left" | "right" | "none",<br />
  "euaTomorrowComment" : text,<br />
  "fbRemovalTomorrow" : "both" | "left" | "right" | "none",<br />
  "fbRemovalTomorrowComment" : text,<br />
  "middleEarExploreMyringotomyTomorrow" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyTomorrowComment" : text,<br />
  "cerumenTomorrow" : "both" | "left" | "right" | "none",<br />
  "cerumentTomorrowComment" : text,<br />
  "granulomaTomorrow" : "both" | "left" | "right" | "none",<br />
  "granulomaTomorrowComment" : text,<br />
  "septorhinoplastyTomorrow" : true | false<br />
  "septorhinoplastyTomorrowComment" : text,<br />
  "scarRevisionCleftLipTomorrow" : true | false <br />
  "scarRevisionCleftLipTomorrowComment" : text,<br />
  "frenulectomyTomorrow" : true | false, <br />
  "frenulectomyTomorrowComment" : text,<br />
<br />
  "tubesFuture" : "both" | "left" | "right" | "none",<br />
  "tubesFutureComment" : text,<br />
  "tPlastyFuture" : "both" | "left" | "right" | "none",<br />
  "tPlastyFutureComment" : text,<br />
  "euaFuture" : "both" | "left" | "right" | "none",<br />
  "euaFutureComment" : text,<br />
  "fbRemovalFuture" : "both" | "left" | "right" | "none",<br />
  "fbRemovalComment" : text,<br />
  "middleEarExploreMyringotomyFuture" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyFutureComment" : text,<br />
  "cerumenFuture" : "both" | "left" | "right" | "none",<br />
  "cerumenFutureComment" : text,<br />
  "granulomaFuture" : "both" | "left" | "right" | "none",<br />
  "granulomaFutureComment" : text,<br />
  "septorhinoplastyFuture" : true | false <br />
  "septorhinoplastyFutureComment" : text,<br />
  "scarRevisionCleftLipFuture" : true | false <br />
  "scarRevisionCleftLipFutureComment" : text,<br />
  "frenulectomyFuture" : true | false <br />
  "frenulectomyFutureComment" : text,<br />
  "comment" : text<br />

* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
GET /tscharts/v1/enttreatment/12/ HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json

2c5
{"id":27,"clinic":9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz", "earCleanedSide" : "left", "earCleanedComment" : "", "audiogramSide" : "left", "audiogramComment" : "", "audiogramRightAway" : false, "audiogramRightAwayComment" : "", "tympanogramSide" : "left", "tympanogramComment" : "", "tympanogramRightAway" : true, "tympanogramRightAwayComment" : "", "mastoidDebridedSide" : "left", "mastoidDebridedComment" : "", "mastoidDebridedHearingAidEval" : true, "mastoidDebridedHearingAidEvalComment" : "", "antibioticDrops" : false, "antibioticDropsComment" : "", "antibioticOrally" : false, "antibioticOrallyComment" : "", "antibioticAcuteInfection" : true, "antibioticAcuteInfectionComment" : "", "antibioticAfterWaterExposureInfectionPrevention" : true, "antibioticAfterWaterExposureInfectionPreventionComment" : "", "boricAcidToday" : false, "boricAcidTodayComment" : "", "boricAcidForHomeUse" : true, "boricAcidForHomeUseComment" : "", "boricAcidSide" : "left", "boricAcidSideComment" : "", "foreignBodyRemoved" : "right", "foreignBodyRemovedComment" : "", "return3Months" : false, "return6Months" : true, "returnPrn" : false, "returnComment" : "", "referredPvtENTEnsenada" : false, "referredPvtENTEnsenadaComment" : "", "referredChildrensHospitalTJ" : true, "referredChildrensHospitalTJComment" : "", "tubesTomorrow" : "left", "tubesTomorrowComment" : "", "tPlastyTomorrow" : "left", "tPlastyTomorrowComment" : "", "euaTomorrow" : "left", "euaTomorrowComment" : "", "fbRemovalTomorrow" : "left", "fbRemovalTomorrowComment" : "", "middleEarExploreMyringotomyTomorrow" : "left", "middleEarExploreMyringotomyTomorrowComment" : "", "cerumenTomorrow" : "left", "cerumentTomorrowComment" : "", "granulomaTomorrow" : "left", "granulomaTomorrowComment" : "", "septorhinoplastyTomorrow" : false, "septorhinoplastyTomorrowComment" : "", "scarRevisionCleftLipTomorrow" : false, "scarRevisionCleftLipTomorrowComment" : "", "frenulectomyTomorrow" : true, "frenulectomyTomorrowComment" : "", "tubesFuture" : "right", "tubesFutureComment" : "", "tPlastyFuture" : "right", "tPlastyFutureComment" : "", "euaFuture" : "right", "euaFutureComment" : "", "fbRemovalFuture" : "right", "fbRemovalComment" : "", "middleEarExploreMyringotomyFuture" : "right", "middleEarExploreMyringotomyFutureComment" : "", "cerumenFuture" : "right", "cerumenFutureComment" : "", "granulomaFuture" : "right", "granulomaFutureComment" : "", "septorhinoplastyFuture" : false, "septorhinoplastyFutureComment" : "", "scarRevisionCleftLipFuture" : false, "scarRevisionCleftLipFutureComment" : "", "frenulectomyFuture" : false, "frenulectomyFutureComment" : "", "comment" : ""}
```
  
**Get Multiple ENT Treatments**
----
  Returns data for all matching ENT treatment resources. A given patient 
may have multiple treatments depending on his or her condition for a given
clinic.

* **URL**

  /tscharts/v1/enttreatment/

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**

   One or more of the following are used to filter the results. 

  "clinic" : id, <br />
  "patient" : id, <br />
  "time" : UTC date time string, <br />
  "earCleanedSide" : "both" | "left" | "right" | "none",<br />
  "audiogramSide" : "both" | "left" | "right" | "none", <br />
  "audiogramRightAway" : true | false<br />
  "tympanogramSide" : "both" | "left" | "right" | "none",<br />
  "tympanogramRightAway" : true | false, <br />
  "mastoidDebridedSide" : "both" | "left" | "right" | "none",<br />
  "mastoidDebridedHearingAidEval" : true | false,<br />
  "antibioticDrops" : true | false <br />
  "antibioticOrally" : true | false <br />
  "antibioticAcuteInfection" : true | false,<br />
  "antibioticAfterWaterExposureInfectionPrevention" : true | false,<br />
  "boricAcidToday" : true | false<br />
  "boricAcidForHomeUse" : true | false, <br />
  "boricAcidSide" : "both" | "left" | "right" | "none",<br />
  "foreignBodyRemoved" : <br />
  "return3Months" : true | false <br />
  "return6Months" : true | false, <br />
  "returnPrn" : true | false <br />
  "referredPvtENTEnsenada" : true | false <br />
  "referredChildrensHospitalTJ" : true | false,<br />
  "tubesTomorrow" : "both" | "left" | "right" | "none",<br />
  "tPlastyTomorrow" : "both" | "left" | "right" | "none",<br />
  "euaTomorrow" : "both" | "left" | "right" | "none",<br />
  "fbRemovalTomorrow" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyTomorrow" : "both" | "left" | "right" | "none",<br />
  "cerumenTomorrow" : "both" | "left" | "right" | "none",<br />
  "granulomaTomorrow" : "both" | "left" | "right" | "none",<br />
  "septorhinoplastyTomorrow" : true | false<br />
  "scarRevisionCleftLipTomorrow" : true | false <br />
  "frenulectomyTomorrow" : true | false, <br />
  "tubesFuture" : "both" | "left" | "right" | "none",<br />
  "tPlastyFuture" : "both" | "left" | "right" | "none",<br />
  "euaFuture" : "both" | "left" | "right" | "none",<br />
  "fbRemovalFuture" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyFuture" : "both" | "left" | "right" | "none",<br />
  "cerumenFuture" : "both" | "left" | "right" | "none",<br />
  "granulomaFuture" : "both" | "left" | "right" | "none",<br />
  "septorhinoplastyFuture" : true | false <br />
  "scarRevisionCleftLipFuture" : true | false <br />
  "frenulectomyFuture" : true | false <br />

* **Data Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 

    [{"id":27,"clinic":9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz", "earCleanedSide" : "left", "earCleanedComment" : "", "audiogramSide" : "left", "audiogramComment" : "", "audiogramRightAway" : false, "audiogramRightAwayComment" : "", "tympanogramSide" : "left", "tympanogramComment" : "", "tympanogramRightAway" : true, "tympanogramRightAwayComment" : "", "mastoidDebridedSide" : "left", "mastoidDebridedComment" : "", "mastoidDebridedHearingAidEval" : true, "mastoidDebridedHearingAidEvalComment" : "", "antibioticDrops" : false, "antibioticDropsComment" : "", "antibioticOrally" : false, "antibioticOrallyComment" : "", "antibioticAcuteInfection" : true, "antibioticAcuteInfectionComment" : "", "antibioticAfterWaterExposureInfectionPrevention" : true, "antibioticAfterWaterExposureInfectionPreventionComment" : "", "boricAcidToday" : false, "boricAcidTodayComment" : "", "boricAcidForHomeUse" : true, "boricAcidForHomeUseComment" : "", "boricAcidSide" : "left", "boricAcidSideComment" : "", "foreignBodyRemoved" : "right", "foreignBodyRemovedComment" : "", "return3Months" : false, "return6Months" : true, "returnPrn" : false, "returnComment" : "", "referredPvtENTEnsenada" : false, "referredPvtENTEnsenadaComment" : "", "referredChildrensHospitalTJ" : true, "referredChildrensHospitalTJComment" : "", "tubesTomorrow" : "left", "tubesTomorrowComment" : "", "tPlastyTomorrow" : "left", "tPlastyTomorrowComment" : "", "euaTomorrow" : "left", "euaTomorrowComment" : "", "fbRemovalTomorrow" : "left", "fbRemovalTomorrowComment" : "", "middleEarExploreMyringotomyTomorrow" : "left", "middleEarExploreMyringotomyTomorrowComment" : "", "cerumenTomorrow" : "left", "cerumentTomorrowComment" : "", "granulomaTomorrow" : "left", "granulomaTomorrowComment" : "", "septorhinoplastyTomorrow" : false, "septorhinoplastyTomorrowComment" : "", "scarRevisionCleftLipTomorrow" : false, "scarRevisionCleftLipTomorrowComment" : "", "frenulectomyTomorrow" : true, "frenulectomyTomorrowComment" : "", "tubesFuture" : "right", "tubesFutureComment" : "", "tPlastyFuture" : "right", "tPlastyFutureComment" : "", "euaFuture" : "right", "euaFutureComment" : "", "fbRemovalFuture" : "right", "fbRemovalComment" : "", "middleEarExploreMyringotomyFuture" : "right", "middleEarExploreMyringotomyFutureComment" : "", "cerumenFuture" : "right", "cerumenFutureComment" : "", "granulomaFuture" : "right", "granulomaFutureComment" : "", "septorhinoplastyFuture" : false, "septorhinoplastyFutureComment" : "", "scarRevisionCleftLipFuture" : false, "scarRevisionCleftLipFutureComment" : "", "frenulectomyFuture" : false, "frenulectomyFutureComment" : "", "comment" : ""}, ...]

* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 403 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
GET /tscharts/v1/enttreatment/?clinic=3 HTTP/1.1
Host: localhost
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:24 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


859
    [{"id":27,"clinic":9,"patient":6,"time":"2017-12-11T01:02:24","username":"xxyyzz", "earCleanedSide" : "left", "earCleanedComment" : "", "audiogramSide" : "left", "audiogramComment" : "", "audiogramRightAway" : false, "audiogramRightAwayComment" : "", "tympanogramSide" : "left", "tympanogramComment" : "", "tympanogramRightAway" : true, "tympanogramRightAwayComment" : "", "mastoidDebridedSide" : "left", "mastoidDebridedComment" : "", "mastoidDebridedHearingAidEval" : true, "mastoidDebridedHearingAidEvalComment" : "", "antibioticDrops" : false, "antibioticDropsComment" : "", "antibioticOrally" : false, "antibioticOrallyComment" : "", "antibioticAcuteInfection" : true, "antibioticAcuteInfectionComment" : "", "antibioticAfterWaterExposureInfectionPrevention" : true, "antibioticAfterWaterExposureInfectionPreventionComment" : "", "boricAcidToday" : false, "boricAcidTodayComment" : "", "boricAcidForHomeUse" : true, "boricAcidForHomeUseComment" : "", "boricAcidSide" : "left", "boricAcidSideComment" : "", "foreignBodyRemoved" : "right", "foreignBodyRemovedComment" : "", "return3Months" : false, "return6Months" : true, "returnPrn" : false, "returnComment" : "", "referredPvtENTEnsenada" : false, "referredPvtENTEnsenadaComment" : "", "referredChildrensHospitalTJ" : true, "referredChildrensHospitalTJComment" : "", "tubesTomorrow" : "left", "tubesTomorrowComment" : "", "tPlastyTomorrow" : "left", "tPlastyTomorrowComment" : "", "euaTomorrow" : "left", "euaTomorrowComment" : "", "fbRemovalTomorrow" : "left", "fbRemovalTomorrowComment" : "", "middleEarExploreMyringotomyTomorrow" : "left", "middleEarExploreMyringotomyTomorrowComment" : "", "cerumenTomorrow" : "left", "cerumentTomorrowComment" : "", "granulomaTomorrow" : "left", "granulomaTomorrowComment" : "", "septorhinoplastyTomorrow" : false, "septorhinoplastyTomorrowComment" : "", "scarRevisionCleftLipTomorrow" : false, "scarRevisionCleftLipTomorrowComment" : "", "frenulectomyTomorrow" : true, "frenulectomyTomorrowComment" : "", "tubesFuture" : "right", "tubesFutureComment" : "", "tPlastyFuture" : "right", "tPlastyFutureComment" : "", "euaFuture" : "right", "euaFutureComment" : "", "fbRemovalFuture" : "right", "fbRemovalComment" : "", "middleEarExploreMyringotomyFuture" : "right", "middleEarExploreMyringotomyFutureComment" : "", "cerumenFuture" : "right", "cerumenFutureComment" : "", "granulomaFuture" : "right", "granulomaFutureComment" : "", "septorhinoplastyFuture" : false, "septorhinoplastyFutureComment" : "", "scarRevisionCleftLipFuture" : false, "scarRevisionCleftLipFutureComment" : "", "frenulectomyFuture" : false, "frenulectomyFutureComment" : "", "comment" : ""}, ...]
0
```
  
**Create an ENT Treatment**
----
  Create an ENT treatment resource for a patient at a specific clinic.

* **URL**

  /tscharts/v1/enttreatment/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**
 
  "clinic" : clinic id, <br />
  "patient" : patient id, <br />
  "earCleanedSide" : "both" | "left" | "right" | "none",<br />
  "earCleanedComment" : text<br />
  "audiogramSide" : "both" | "left" | "right" | "none", <br />
  "audiogramComment" : text,<br />
  "audiogramRightAway" : true | false<br />
  "audiogramRightAwayComment" : text,<br />
  "tympanogramSide" : "both" | "left" | "right" | "none",<br />
  "tympanogramComment" : text,<br />
  "tympanogramRightAway" : true | false, <br />
  "tympanogramRightAwayComment" : text,<br />
  "mastoidDebridedSide" : "both" | "left" | "right" | "none",<br />
  "mastoidDebridedComment" : text,<br />
  "mastoidDebridedHearingAidEval" : true | false,<br />
  "mastoidDebridedHearingAidEvalComment" : text,<br />
  "antibioticDrops" : true | false <br />
  "antibioticDropsComment" : text,<br />
  "antibioticOrally" : true | false <br />
  "antibioticOrallyComment" : text,<br />
  "antibioticAcuteInfection" : true | false,<br />
  "antibioticAcuteInfectionComment" : text,<br />
  "antibioticAfterWaterExposureInfectionPrevention" : true | false,<br />
  "antibioticAfterWaterExposureInfectionPreventionComment" : text,<br />
  "boricAcidToday" : true | false<br />
  "boricAcidTodayComment" : text,<br />
  "boricAcidForHomeUse" : true | false, <br />
  "boricAcidForHomeUseComment" : text,<br />
  "boricAcidSide" : "both" | "left" | "right" | "none",<br />
  "boricAcidSideComment" : text,<br />
  "foreignBodyRemoved" : <br />
  "foreignBodyRemovedComment" : text,<br />
  "return3Months" : true | false <br />
  "return6Months" : true | false, <br />
  "returnPrn" : true | false <br />
  "returnComment" : text,<br />
  "referredPvtENTEnsenada" : true | false <br />
  "referredPvtENTEnsenadaComment" : text,<br />
  "referredChildrensHospitalTJ" : true | false,<br />
  "referredChildrensHospitalTJComment" : text,<br />
  "tubesTomorrow" : "both" | "left" | "right" | "none",<br />
  "tubesTomorrowComment" : text,<br />
  "tPlastyTomorrow" : "both" | "left" | "right" | "none",<br />
  "tPlastyTomorrowComment" : text,<br />
  "euaTomorrow" : "both" | "left" | "right" | "none",<br />
  "euaTomorrowComment" : text,<br />
  "fbRemovalTomorrow" : "both" | "left" | "right" | "none",<br />
  "fbRemovalTomorrowComment" : text,<br />
  "middleEarExploreMyringotomyTomorrow" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyTomorrowComment" : text,<br />
  "cerumenTomorrow" : "both" | "left" | "right" | "none",<br />
  "cerumentTomorrowComment" : text,<br />
  "granulomaTomorrow" : "both" | "left" | "right" | "none",<br />
  "granulomaTomorrowComment" : text,<br />
  "septorhinoplastyTomorrow" : true | false<br />
  "septorhinoplastyTomorrowComment" : text,<br />
  "scarRevisionCleftLipTomorrow" : true | false <br />
  "scarRevisionCleftLipTomorrowComment" : text,<br />
  "frenulectomyTomorrow" : true | false, <br />
  "frenulectomyTomorrowComment" : text,<br />
  "tubesFuture" : "both" | "left" | "right" | "none",<br />
  "tubesFutureComment" : text,<br />
  "tPlastyFuture" : "both" | "left" | "right" | "none",<br />
  "tPlastyFutureComment" : text,<br />
  "euaFuture" : "both" | "left" | "right" | "none",<br />
  "euaFutureComment" : text,<br />
  "fbRemovalFuture" : "both" | "left" | "right" | "none",<br />
  "fbRemovalComment" : text,<br />
  "middleEarExploreMyringotomyFuture" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyFutureComment" : text,<br />
  "cerumenFuture" : "both" | "left" | "right" | "none",<br />
  "cerumenFutureComment" : text,<br />
  "granulomaFuture" : "both" | "left" | "right" | "none",<br />
  "granulomaFutureComment" : text,<br />
  "septorhinoplastyFuture" : true | false <br />
  "septorhinoplastyFutureComment" : text,<br />
  "scarRevisionCleftLipFuture" : true | false <br />
  "scarRevisionCleftLipFutureComment" : text,<br />
  "frenulectomyFuture" : true | false <br />
  "frenulectomyFutureComment" : text,<br />
  "comment" : text<br />

   **Optional:**

   None 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "id" : id }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
POST /tscharts/v1/enttreatment/ HTTP/1.1
Host: localhost
Content-Length: 738
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{"clinic":9,"patient":6,"username":"xxyyzz", "earCleanedSide" : "left", "earCleanedComment" : "", "audiogramSide" : "left", "audiogramComment" : "", "audiogramRightAway" : false, "audiogramRightAwayComment" : "", "tympanogramSide" : "left", "tympanogramComment" : "", "tympanogramRightAway" : true, "tympanogramRightAwayComment" : "", "mastoidDebridedSide" : "left", "mastoidDebridedComment" : "", "mastoidDebridedHearingAidEval" : true, "mastoidDebridedHearingAidEvalComment" : "", "antibioticDrops" : false, "antibioticDropsComment" : "", "antibioticOrally" : false, "antibioticOrallyComment" : "", "antibioticAcuteInfection" : true, "antibioticAcuteInfectionComment" : "", "antibioticAfterWaterExposureInfectionPrevention" : true, "antibioticAfterWaterExposureInfectionPreventionComment" : "", "boricAcidToday" : false, "boricAcidTodayComment" : "", "boricAcidForHomeUse" : true, "boricAcidForHomeUseComment" : "", "boricAcidSide" : "left", "boricAcidSideComment" : "", "foreignBodyRemoved" : "right", "foreignBodyRemovedComment" : "", "return3Months" : false, "return6Months" : true, "returnPrn" : false, "returnComment" : "", "referredPvtENTEnsenada" : false, "referredPvtENTEnsenadaComment" : "", "referredChildrensHospitalTJ" : true, "referredChildrensHospitalTJComment" : "", "tubesTomorrow" : "left", "tubesTomorrowComment" : "", "tPlastyTomorrow" : "left", "tPlastyTomorrowComment" : "", "euaTomorrow" : "left", "euaTomorrowComment" : "", "fbRemovalTomorrow" : "left", "fbRemovalTomorrowComment" : "", "middleEarExploreMyringotomyTomorrow" : "left", "middleEarExploreMyringotomyTomorrowComment" : "", "cerumenTomorrow" : "left", "cerumentTomorrowComment" : "", "granulomaTomorrow" : "left", "granulomaTomorrowComment" : "", "septorhinoplastyTomorrow" : false, "septorhinoplastyTomorrowComment" : "", "scarRevisionCleftLipTomorrow" : false, "scarRevisionCleftLipTomorrowComment" : "", "frenulectomyTomorrow" : true, "frenulectomyTomorrowComment" : "", "tubesFuture" : "right", "tubesFutureComment" : "", "tPlastyFuture" : "right", "tPlastyFutureComment" : "", "euaFuture" : "right", "euaFutureComment" : "", "fbRemovalFuture" : "right", "fbRemovalComment" : "", "middleEarExploreMyringotomyFuture" : "right", "middleEarExploreMyringotomyFutureComment" : "", "cerumenFuture" : "right", "cerumenFutureComment" : "", "granulomaFuture" : "right", "granulomaFutureComment" : "", "septorhinoplastyFuture" : false, "septorhinoplastyFutureComment" : "", "scarRevisionCleftLipFuture" : false, "scarRevisionCleftLipFutureComment" : "", "frenulectomyFuture" : false, "frenulectomyFutureComment" : "", "comment" : ""} HTTP/1.1 200 OK
Date: Mon, 11 Dec 2017 01:02:23 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept
X-Frame-Options: SAMEORIGIN
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
Transfer-Encoding: chunked
Content-Type: application/json


8
{"id":2}
0
```

**Update an ENT Treatment**
----
  Update an ENT treatment instance

* **URL**

  /tscharts/v1/enttreatment/id

* **Method:**

  `PUT`
  
*  **URL Params**

   None

* **Data Params**

   **Required:**

   One or more of the following field/value pairs

  "clinic" : clinic id, <br />
  "patient" : patient id, <br />
  "earCleanedSide" : "both" | "left" | "right" | "none",<br />
  "earCleanedComment" : text<br />
  "audiogramSide" : "both" | "left" | "right" | "none", <br />
  "audiogramComment" : text,<br />
  "audiogramRightAway" : true | false<br />
  "audiogramRightAwayComment" : text,<br />
  "tympanogramSide" : "both" | "left" | "right" | "none",<br />
  "tympanogramComment" : text,<br />
  "tympanogramRightAway" : true | false, <br />
  "tympanogramRightAwayComment" : text,<br />
  "mastoidDebridedSide" : "both" | "left" | "right" | "none",<br />
  "mastoidDebridedComment" : text,<br />
  "mastoidDebridedHearingAidEval" : true | false,<br />
  "mastoidDebridedHearingAidEvalComment" : text,<br />
  "antibioticDrops" : true | false <br />
  "antibioticDropsComment" : text,<br />
  "antibioticOrally" : true | false <br />
  "antibioticOrallyComment" : text,<br />
  "antibioticAcuteInfection" : true | false,<br />
  "antibioticAcuteInfectionComment" : text,<br />
  "antibioticAfterWaterExposureInfectionPrevention" : true | false,<br />
  "antibioticAfterWaterExposureInfectionPreventionComment" : text,<br />
  "boricAcidToday" : true | false<br />
  "boricAcidTodayComment" : text,<br />
  "boricAcidForHomeUse" : true | false, <br />
  "boricAcidForHomeUseComment" : text,<br />
  "boricAcidSide" : "both" | "left" | "right" | "none",<br />
  "boricAcidSideComment" : text,<br />
  "foreignBodyRemoved" : <br />
  "foreignBodyRemovedComment" : text,<br />
  "return3Months" : true | false <br />
  "return6Months" : true | false, <br />
  "returnPrn" : true | false <br />
  "returnComment" : text,<br />
  "referredPvtENTEnsenada" : true | false <br />
  "referredPvtENTEnsenadaComment" : text,<br />
  "referredChildrensHospitalTJ" : true | false,<br />
  "referredChildrensHospitalTJComment" : text,<br />
  "tubesTomorrow" : "both" | "left" | "right" | "none",<br />
  "tubesTomorrowComment" : text,<br />
  "tPlastyTomorrow" : "both" | "left" | "right" | "none",<br />
  "tPlastyTomorrowComment" : text,<br />
  "euaTomorrow" : "both" | "left" | "right" | "none",<br />
  "euaTomorrowComment" : text,<br />
  "fbRemovalTomorrow" : "both" | "left" | "right" | "none",<br />
  "fbRemovalTomorrowComment" : text,<br />
  "middleEarExploreMyringotomyTomorrow" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyTomorrowComment" : text,<br />
  "cerumenTomorrow" : "both" | "left" | "right" | "none",<br />
  "cerumentTomorrowComment" : text,<br />
  "granulomaTomorrow" : "both" | "left" | "right" | "none",<br />
  "granulomaTomorrowComment" : text,<br />
  "septorhinoplastyTomorrow" : true | false<br />
  "septorhinoplastyTomorrowComment" : text,<br />
  "scarRevisionCleftLipTomorrow" : true | false <br />
  "scarRevisionCleftLipTomorrowComment" : text,<br />
  "frenulectomyTomorrow" : true | false, <br />
  "frenulectomyTomorrowComment" : text,<br />
  "tubesFuture" : "both" | "left" | "right" | "none",<br />
  "tubesFutureComment" : text,<br />
  "tPlastyFuture" : "both" | "left" | "right" | "none",<br />
  "tPlastyFutureComment" : text,<br />
  "euaFuture" : "both" | "left" | "right" | "none",<br />
  "euaFutureComment" : text,<br />
  "fbRemovalFuture" : "both" | "left" | "right" | "none",<br />
  "fbRemovalComment" : text,<br />
  "middleEarExploreMyringotomyFuture" : "both" | "left" | "right" | "none",<br />
  "middleEarExploreMyringotomyFutureComment" : text,<br />
  "cerumenFuture" : "both" | "left" | "right" | "none",<br />
  "cerumenFutureComment" : text,<br />
  "granulomaFuture" : "both" | "left" | "right" | "none",<br />
  "granulomaFutureComment" : text,<br />
  "septorhinoplastyFuture" : true | false <br />
  "septorhinoplastyFutureComment" : text,<br />
  "scarRevisionCleftLipFuture" : true | false <br />
  "scarRevisionCleftLipFutureComment" : text,<br />
  "frenulectomyFuture" : true | false <br />
  "frenulectomyFutureComment" : text,<br />
  "comment" : text<br />

* **Success Response:**

  * **Code:** 200 <br />
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST<br />
  * **Code:** 404 NOT FOUND<br />
  * **Code:** 500 SERVER ERROR

* **Example:**

```
PUT /tscharts/v1/enttreatment/24/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 18
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae


{"granulomaFuture": "both"}HTTP/1.0 200 OK
Date: Sun, 23 Apr 2017 01:19:21 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

**Delete an ENT Treatment**
----
  Delete an ENT treatment resource. Use is not recommended except for unit test applications.

* **URL**

  /tscharts/v1/enttreatment/id

* **Method:**

  `DELETE`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** None
 
* **Error Response:**

  * **Code:** 404 NOT FOUND

* **Example:**

```
DELETE /tscharts/v1/enttreatment/140/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 2
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: python-requests/2.2.1 CPython/2.7.6 Linux/4.2.0-27-generic
Content-Type: application/json
Authorization: Token 53f29e4dfc917c28a0e71f26525307250f1f8101


{}HTTP/1.0 200 OK
Date: Fri, 21 Apr 2017 05:52:49 GMT
Server: WSGIServer/0.1 Python/2.7.6
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS


{}
```

