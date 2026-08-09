//(C) Copyright Syd Logan 2026
//(C) Copyright Thousand Smiles Foundation 2026
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//
//You may obtain a copy of the License at
//http://www.apache.org/licenses/LICENSE-2.0
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

use anyhow::{anyhow, Result};
use chrono::NaiveDate;
use serde::de::Deserializer;
use serde::{Deserialize, Serialize};

use crate::clinic_filter::Clinic;

/// Accept JSON null as empty string (Django may omit or null some fields).
fn string_null_default<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    Ok(Option::<String>::deserialize(deserializer)?.unwrap_or_default())
}

/// API returns oldid as int; docs sometimes show string.
fn oldid_as_string<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    let v = Option::<serde_json::Value>::deserialize(deserializer)?;
    Ok(match v {
        None | Some(serde_json::Value::Null) => String::new(),
        Some(serde_json::Value::Number(n)) => n.to_string(),
        Some(serde_json::Value::String(s)) => s,
        Some(other) => other.to_string(),
    })
}

/// Normalize patient JSON from tscharts (e.g. numeric `oldid`) before typed parse.
pub fn patient_from_value(mut v: serde_json::Value) -> Result<Patient> {
    if let Some(obj) = v.as_object_mut() {
        if let Some(oldid) = obj.get("oldid").cloned() {
            let as_str = match oldid {
                serde_json::Value::Null => String::new(),
                serde_json::Value::Number(n) => n.to_string(),
                serde_json::Value::String(s) => s,
                other => other.to_string(),
            };
            obj.insert("oldid".into(), serde_json::Value::String(as_str));
        }
        for key in [
            "first",
            "middle",
            "paternal_last",
            "maternal_last",
            "suffix",
            "prefix",
            "dob",
            "gender",
            "street1",
            "street2",
            "city",
            "colonia",
            "state",
            "phone1",
            "phone2",
            "email",
            "emergencyfullname",
            "emergencyphone",
            "emergencyemail",
            "curp",
        ] {
            if matches!(obj.get(key), Some(serde_json::Value::Null)) {
                obj.insert(key.into(), serde_json::Value::String(String::new()));
            }
        }
    }
    serde_json::from_value(v).map_err(|e| anyhow!("patient JSON: {e}"))
}

#[derive(Debug, Deserialize)]
pub struct LoginResponse {
    pub token: String,
    #[serde(default)]
    pub id: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct ClinicDto {
    pub id: i64,
    /// API JSON field is `location`; Rust/UI use `place` (clinic site name).
    #[serde(rename = "location")]
    pub place: String,
    pub start: String,
    pub end: String,
}

impl ClinicDto {
    pub fn into_clinic(self) -> Result<Clinic> {
        Ok(Clinic {
            id: self.id,
            place: self.place,
            start: parse_mdy(&self.start)?,
            end: parse_mdy(&self.end)?,
        })
    }
}

fn parse_mdy(s: &str) -> Result<NaiveDate> {
    NaiveDate::parse_from_str(s, "%m/%d/%Y")
        .or_else(|_| NaiveDate::parse_from_str(s, "%m-%d-%Y"))
        .map_err(|e| anyhow!("bad date '{s}': {e}"))
}

pub fn format_mdy(d: NaiveDate) -> String {
    d.format("%m/%d/%Y").to_string()
}

/// e.g. "Friday 02/06/2026"
pub fn format_weekday_mdy(d: NaiveDate) -> String {
    d.format("%A %m/%d/%Y").to_string()
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Registration {
    pub id: i64,
    pub patient: i64,
    pub clinic: i64,
    #[serde(default)]
    pub state: Option<String>,
    #[serde(default)]
    pub timein: Option<String>,
    #[serde(default)]
    pub timeout: Option<String>,
}

/// Full image payload from GET /image/{id}/ or newest=true list endpoint.
#[derive(Debug, Clone, Deserialize)]
pub struct ImagePayload {
    pub id: i64,
    pub patient: i64,
    #[serde(default)]
    pub clinic: Option<i64>,
    #[serde(default)]
    pub station: Option<i64>,
    #[serde(rename = "type")]
    pub kind: String,
    /// Base64 image bytes (may include a data: URL prefix).
    pub data: String,
}

#[derive(Debug, Clone, Deserialize, Serialize, Default)]
pub struct Patient {
    #[serde(default)]
    pub id: Option<i64>,
    #[serde(default, deserialize_with = "string_null_default")]
    pub first: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub middle: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub paternal_last: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub maternal_last: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub suffix: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub prefix: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub dob: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub gender: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub street1: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub street2: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub city: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub colonia: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub state: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub phone1: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub phone2: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub email: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub emergencyfullname: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub emergencyphone: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub emergencyemail: String,
    #[serde(default, deserialize_with = "string_null_default")]
    pub curp: String,
    #[serde(default, deserialize_with = "oldid_as_string")]
    pub oldid: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn patient_deserializes_numeric_oldid() {
        let json = r#"{
            "id": 27,
            "first": "Fred",
            "middle": "",
            "paternal_last": "Flintstone",
            "maternal_last": "Rubble",
            "suffix": "",
            "prefix": "",
            "dob": "04/01/1962",
            "gender": "Male",
            "street1": "123 Rock",
            "street2": null,
            "city": "Bedrock",
            "colonia": "",
            "state": "Baja California",
            "phone1": "",
            "phone2": "",
            "email": "",
            "emergencyfullname": "",
            "emergencyphone": "",
            "emergencyemail": "",
            "curp": "",
            "oldid": -1
        }"#;
        let p: Patient = serde_json::from_str(json).expect("deserialize");
        assert_eq!(p.first, "Fred");
        assert_eq!(p.paternal_last, "Flintstone");
        assert_eq!(p.dob, "04/01/1962");
        assert_eq!(p.gender, "Male");
        assert_eq!(p.oldid, "-1");
        assert_eq!(p.street2, "");
    }

    #[test]
    fn patient_deserializes_live_edit_payload() {
        let json = r#"{"id":1667,"paternal_last":"Gonzalez","maternal_last":"Millan","first":"Victor","middle":"Adriel","suffix":"","prefix":"","dob":"07/12/2021","gender":"Male","street1":"Callejón Independencia 835","street2":"","city":"Ensenada","colonia":"Maneadero","state":"Baja California","phone1":"6461875176","phone2":"","email":"shikis28@gmail.com","emergencyfullname":"Carmen Maricela Millán Avalo","emergencyphone":"6461991117","emergencyemail":"","curp":"GOMV201712HBCNLCS9","oldid":-1}"#;
        let v: serde_json::Value = serde_json::from_str(json).expect("value");
        let p = patient_from_value(v).expect("patient");
        assert_eq!(p.first, "Victor");
        assert_eq!(p.paternal_last, "Gonzalez");
        assert_eq!(p.oldid, "-1");
        assert_eq!(p.dob, "07/12/2021");
        assert_eq!(p.gender, "Male");
    }
}
