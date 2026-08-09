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

//! HTTP client for the tscharts REST API.

mod types;

pub use types::*;

use anyhow::{anyhow, Context, Result};
use reqwest::header::AUTHORIZATION;
use reqwest::{Client, StatusCode};
use serde::de::DeserializeOwned;
use serde::Serialize;
use serde_json::{json, Map, Value};

use crate::clinic_filter::Clinic;
use crate::config::Config;

/// Django REST framework TokenAuthentication value: `Token <key>`.
fn token_auth(cred: &str) -> String {
    format!("Token {cred}")
}

#[derive(Clone)]
pub struct TschartsClient {
    http: Client,
    base: String,
    /// When set, sent as HTTP Host so Django ALLOWED_HOSTS / nginx `server_name`
    /// accept the request (e.g. base URL is host.docker.internal or an IP).
    host_header: Option<String>,
}

/// Prefer Host: localhost when the configured base hostname would be rejected
/// by Django (underscores) or is a Docker/EC2 reachability name not in ALLOWED_HOSTS.
fn host_header_for_base(base: &str) -> Option<String> {
    let Ok(url) = reqwest::Url::parse(base) else {
        return Some("localhost".into());
    };
    match url.host_str() {
        Some("localhost") | Some("127.0.0.1") | Some("::1") => None,
        Some(h) if h.contains('_') => Some("localhost".into()),
        Some("host.docker.internal") => Some("localhost".into()),
        // Public/private IP via host nginx (server_name localhost) — keep Host valid.
        Some(h) if h.chars().all(|c| c.is_ascii_digit() || c == '.') => Some("localhost".into()),
        _ => None,
    }
}

impl TschartsClient {
    pub fn new(config: &Config) -> Result<Self> {
        let http = Client::builder()
            .danger_accept_invalid_certs(config.tls_insecure)
            .build()
            .context("build reqwest client")?;
        let base = config.tscharts_base_url.clone();
        Ok(Self {
            host_header: host_header_for_base(&base),
            http,
            base,
        })
    }

    fn url(&self, path: &str) -> String {
        format!("{}{}", self.base, path)
    }

    fn with_host(&self, req: reqwest::RequestBuilder) -> reqwest::RequestBuilder {
        match &self.host_header {
            Some(host) => req.header(reqwest::header::HOST, host.as_str()),
            None => req,
        }
    }

    fn get(&self, url: String) -> reqwest::RequestBuilder {
        self.with_host(self.http.get(url))
    }

    fn post(&self, url: String) -> reqwest::RequestBuilder {
        self.with_host(self.http.post(url))
    }

    fn put(&self, url: String) -> reqwest::RequestBuilder {
        self.with_host(self.http.put(url))
    }

    fn delete(&self, url: String) -> reqwest::RequestBuilder {
        self.with_host(self.http.delete(url))
    }

    async fn parse_json<T: DeserializeOwned>(&self, resp: reqwest::Response) -> Result<T> {
        let status = resp.status();
        let text = resp.text().await.unwrap_or_default();
        if !status.is_success() {
            return Err(anyhow!("tscharts HTTP {status}: {text}"));
        }
        if text.trim().is_empty() {
            return Err(anyhow!("tscharts returned empty body for success {status}"));
        }
        serde_json::from_str(&text).with_context(|| format!("decode JSON: {text}"))
    }

    async fn send_empty_ok(&self, resp: reqwest::Response) -> Result<()> {
        let status = resp.status();
        if status.is_success() {
            Ok(())
        } else {
            let text = resp.text().await.unwrap_or_default();
            Err(anyhow!("tscharts HTTP {status}: {text}"))
        }
    }

    pub async fn login(&self, username: &str, password: &str) -> Result<LoginResponse> {
        let body = json!({ "username": username, "password": password });
        let resp = self
            .post(self.url("/tscharts/v1/login/"))
            .json(&body)
            .send()
            .await
            .context("login request")?;
        self.parse_json(resp).await
    }

    pub async fn list_clinics(&self, cred: &str) -> Result<Vec<Clinic>> {
        let resp = self
            .get(self.url("/tscharts/v1/clinic/"))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("list clinics")?;
        let raw: Vec<ClinicDto> = self.parse_json(resp).await?;
        raw.into_iter().map(ClinicDto::into_clinic).collect()
    }

    pub async fn get_clinic(&self, cred: &str, id: i64) -> Result<Clinic> {
        let resp = self
            .get(self.url(&format!("/tscharts/v1/clinic/{id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("get clinic")?;
        let raw: ClinicDto = self.parse_json(resp).await?;
        raw.into_clinic()
    }

    pub async fn create_clinic(
        &self,
        cred: &str,
        place: &str,
        start: &str,
        end: &str,
    ) -> Result<i64> {
        let body = json!({
            "location": place,
            "start": start,
            "end": end,
        });
        let resp = self
            .post(self.url("/tscharts/v1/clinic/"))
            .header(AUTHORIZATION, token_auth(cred))
            .json(&body)
            .send()
            .await
            .context("create clinic")?;
        let v: Value = self.parse_json(resp).await?;
        v.get("id")
            .and_then(|x| x.as_i64())
            .ok_or_else(|| anyhow!("create clinic: no id in {v}"))
    }

    pub async fn update_clinic(
        &self,
        cred: &str,
        id: i64,
        place: &str,
        start: &str,
        end: &str,
    ) -> Result<()> {
        let body = json!({
            "location": place,
            "start": start,
            "end": end,
        });
        let resp = self
            .put(self.url(&format!("/tscharts/v1/clinic/{id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .json(&body)
            .send()
            .await
            .context("update clinic")?;
        self.send_empty_ok(resp).await
    }

    pub async fn delete_clinic(&self, cred: &str, id: i64) -> Result<()> {
        let resp = self
            .delete(self.url(&format!("/tscharts/v1/clinic/{id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("delete clinic")?;
        self.send_empty_ok(resp).await
    }

    pub async fn list_enrollments(&self, cred: &str, clinic_id: i64) -> Result<Vec<Registration>> {
        let resp = self
            .get(self.url(&format!(
                "/tscharts/v1/register/?clinic={clinic_id}"
            )))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("list enrollments")?;
        if resp.status() == StatusCode::NOT_FOUND {
            return Ok(vec![]);
        }
        self.parse_json(resp).await
    }

    pub async fn list_enrollments_for_patient(
        &self,
        cred: &str,
        patient_id: i64,
    ) -> Result<Vec<Registration>> {
        let resp = self
            .get(self.url(&format!(
                "/tscharts/v1/register/?patient={patient_id}"
            )))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("list enrollments for patient")?;
        if resp.status() == StatusCode::NOT_FOUND {
            return Ok(vec![]);
        }
        self.parse_json(resp).await
    }

    pub async fn create_enrollment(
        &self,
        cred: &str,
        clinic_id: i64,
        patient_id: i64,
    ) -> Result<i64> {
        let body = json!({ "clinic": clinic_id, "patient": patient_id });
        let resp = self
            .post(self.url("/tscharts/v1/register/"))
            .header(AUTHORIZATION, token_auth(cred))
            .json(&body)
            .send()
            .await
            .context("create enrollment")?;
        if resp.status() == StatusCode::CONFLICT {
            return Err(anyhow!(
                "patient already checked in today for this clinic (unregister that row first, or register again on another day)"
            ));
        }
        let v: Value = self.parse_json(resp).await?;
        v.get("id")
            .and_then(|x| x.as_i64())
            .ok_or_else(|| anyhow!("create enrollment: no id"))
    }

    pub async fn delete_enrollment(&self, cred: &str, enroll_id: i64) -> Result<()> {
        let resp = self
            .delete(self.url(&format!("/tscharts/v1/register/{enroll_id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("delete enrollment")?;
        self.send_empty_ok(resp).await
    }

    pub async fn get_patient(&self, cred: &str, id: i64) -> Result<Patient> {
        let resp = self
            .get(self.url(&format!("/tscharts/v1/patient/{id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("get patient")?;
        let v: Value = self.parse_json(resp).await?;
        patient_from_value(v)
    }

    pub async fn search_patients(
        &self,
        cred: &str,
        query: &[(&str, String)],
    ) -> Result<Vec<i64>> {
        let mut url = self.url("/tscharts/v1/patient/?");
        for (i, (k, v)) in query.iter().enumerate() {
            if i > 0 {
                url.push('&');
            }
            url.push_str(k);
            url.push('=');
            url.push_str(&urlencoding::encode(v));
        }
        let resp = self
            .get(url)
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("search patients")?;
        if resp.status() == StatusCode::NOT_FOUND {
            return Ok(vec![]);
        }
        self.parse_json(resp).await
    }

    pub async fn create_patient(&self, cred: &str, body: &impl Serialize) -> Result<i64> {
        let resp = self
            .post(self.url("/tscharts/v1/patient/"))
            .header(AUTHORIZATION, token_auth(cred))
            .json(body)
            .send()
            .await
            .context("create patient")?;
        if resp.status() == StatusCode::CONFLICT {
            let text = resp.text().await.unwrap_or_default();
            return Err(anyhow!(
                "Patient already exists (same paternal last, first, DOB, and gender). {text}"
            ));
        }
        let v: Value = self.parse_json(resp).await?;
        v.get("id")
            .and_then(|x| x.as_i64())
            .ok_or_else(|| anyhow!("create patient: no id"))
    }

    pub async fn update_patient(
        &self,
        cred: &str,
        id: i64,
        body: &impl Serialize,
    ) -> Result<()> {
        let resp = self
            .put(self.url(&format!("/tscharts/v1/patient/{id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .json(body)
            .send()
            .await
            .context("update patient")?;
        self.send_empty_ok(resp).await
    }

    /// Newest Headshot for a patient (tablet uses patient + type + newest=true).
    pub async fn get_newest_headshot(
        &self,
        cred: &str,
        patient_id: i64,
    ) -> Result<Option<ImagePayload>> {
        let resp = self
            .get(self.url(&format!(
                "/tscharts/v1/image/?patient={patient_id}&type=Headshot&newest=true"
            )))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("get newest headshot")?;
        if resp.status() == StatusCode::NOT_FOUND {
            return Ok(None);
        }
        let img: ImagePayload = self.parse_json(resp).await?;
        Ok(Some(img))
    }

    pub async fn list_headshot_ids(&self, cred: &str, patient_id: i64) -> Result<Vec<i64>> {
        let resp = self
            .get(self.url(&format!(
                "/tscharts/v1/image/?patient={patient_id}&type=Headshot&sort=true"
            )))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("list headshots")?;
        if resp.status() == StatusCode::NOT_FOUND {
            return Ok(vec![]);
        }
        self.parse_json(resp).await
    }

    pub async fn create_headshot(
        &self,
        cred: &str,
        patient_id: i64,
        data_b64: &str,
        clinic_id: Option<i64>,
    ) -> Result<i64> {
        let mut map = Map::new();
        map.insert("type".into(), Value::String("Headshot".into()));
        map.insert("patient".into(), json!(patient_id));
        map.insert("data".into(), Value::String(data_b64.to_string()));
        if let Some(c) = clinic_id {
            map.insert("clinic".into(), json!(c));
        }
        let resp = self
            .post(self.url("/tscharts/v1/image/"))
            .header(AUTHORIZATION, token_auth(cred))
            .json(&Value::Object(map))
            .send()
            .await
            .context("create headshot")?;
        let v: Value = self.parse_json(resp).await?;
        v.get("id")
            .and_then(|x| x.as_i64())
            .ok_or_else(|| anyhow!("create headshot: no id"))
    }

    pub async fn delete_image(&self, cred: &str, image_id: i64) -> Result<()> {
        let resp = self
            .delete(self.url(&format!("/tscharts/v1/image/{image_id}/")))
            .header(AUTHORIZATION, token_auth(cred))
            .send()
            .await
            .context("delete image")?;
        self.send_empty_ok(resp).await
    }
}
