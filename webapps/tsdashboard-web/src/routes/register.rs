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

use axum::extract::{Path, State};
use axum::response::{IntoResponse, Redirect, Response};
use axum::Form;
use chrono::Local;
use serde::Deserialize;
use tower_sessions::Session;

use crate::clinic_filter::can_register;
use crate::client::format_mdy;
use crate::html::{escape, flash_err, layout};
use crate::session::require_token;
use crate::AppState;

pub async fn register_form(
    State(state): State<AppState>,
    session: Session,
    Path(clinic_id): Path<i64>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let clinic = state
        .api
        .get_clinic(&token, clinic_id)
        .await
        .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?;

    if !can_register(&clinic, today) {
        return Ok(Redirect::to(&format!(
            "/clinics/{clinic_id}?err=Cannot%20register%20for%20a%20future%20clinic"
        ))
        .into_response());
    }

    let body = format!(
        r#"
    <h1>Register patient for clinic {id}</h1>
    <p>{loc} · {start} → {end}</p>
    <form method="post" action="/clinics/{id}/register" class="stack">
      <label>Patient ID <input name="patient_id" type="number" required></label>
      <button type="submit">Register</button>
    </form>
    <p class="muted">Patient must already exist. Use <a href="/patients/new">New patient</a> or <a href="/patients/search">Find patient</a> first. Registration is separate from demographics.</p>
    "#,
        id = clinic_id,
        loc = escape(&clinic.place),
        start = format_mdy(clinic.start),
        end = format_mdy(clinic.end),
    );
    Ok(layout("Register", &body).into_response())
}

#[derive(Deserialize)]
pub struct RegisterForm {
    patient_id: i64,
}

pub async fn register_submit(
    State(state): State<AppState>,
    session: Session,
    Path(clinic_id): Path<i64>,
    Form(form): Form<RegisterForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let clinic = state
        .api
        .get_clinic(&token, clinic_id)
        .await
        .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?;

    if !can_register(&clinic, today) {
        return Ok(Redirect::to(&format!(
            "/clinics/{clinic_id}?err=Cannot%20register%20for%20a%20future%20clinic"
        ))
        .into_response());
    }

    match state
        .api
        .create_enrollment(&token, clinic_id, form.patient_id)
        .await
    {
        Ok(_) => Ok(Redirect::to(&format!(
            "/clinics/{clinic_id}?msg=Patient%20registered"
        ))
        .into_response()),
        Err(e) => Ok(Redirect::to(&format!(
            "/clinics/{clinic_id}?err={}",
            urlencoding::encode(&e.to_string())
        ))
        .into_response()),
    }
}

pub async fn unregister(
    State(state): State<AppState>,
    session: Session,
    Path((clinic_id, register_id)): Path<(i64, i64)>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    state
        .api
        .delete_enrollment(&token, register_id)
        .await
        .map_err(|e| {
            Redirect::to(&format!(
                "/clinics/{clinic_id}?err={}",
                urlencoding::encode(&e.to_string())
            ))
            .into_response()
        })?;
    Ok(Redirect::to(&format!("/clinics/{clinic_id}?msg=Unregistered")).into_response())
}
