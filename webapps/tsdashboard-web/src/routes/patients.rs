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

use axum::extract::{Path, Query, State};
use axum::response::{IntoResponse, Redirect, Response};
use axum::Form;
use serde::Deserialize;
use tower_sessions::Session;

use crate::avatar::headshot_img;
use crate::client::{Patient, TschartsClient};
use crate::html::{escape, flash_err, flash_ok, layout, Html};
use crate::session::require_token;
use crate::AppState;

fn patient_form_fields(p: &Patient, action: &str, submit: &str, dup_watch: bool) -> String {
    let watch = if dup_watch { " data-dup-watch=\"1\"" } else { "" };
    let panel = if dup_watch {
        r#"<div id="dup-matches" class="dup-panel" aria-live="polite"></div>"#
    } else {
        ""
    };
    let script = if dup_watch {
        DUP_CHECK_SCRIPT
    } else {
        ""
    };
    format!(
        r#"
    {panel}
    <form method="post" action="{action}" class="stack two-col" id="patient-form"{watch}>
      <label>First <input name="first" value="{first}" required autocomplete="off"></label>
      <label>Middle <input name="middle" value="{middle}"></label>
      <label>Paternal last <input name="paternal_last" value="{paternal}" required autocomplete="off"></label>
      <label>Maternal last <input name="maternal_last" value="{maternal}" required autocomplete="off"></label>
      <label>Prefix <input name="prefix" value="{prefix}"></label>
      <label>Suffix <input name="suffix" value="{suffix}"></label>
      <label>DOB (mm/dd/YYYY) <input name="dob" value="{dob}" required placeholder="08/08/1992" autocomplete="off"></label>
      <label>Gender
        <select name="gender" required>
          <option value="Male" {male}>Male</option>
          <option value="Female" {female}>Female</option>
        </select>
      </label>
      <label>CURP <input name="curp" value="{curp}" required autocomplete="off"></label>
      <label>Old ID <input name="oldid" value="{oldid}"></label>
      <label>Street 1 <input name="street1" value="{street1}" required></label>
      <label>Street 2 <input name="street2" value="{street2}"></label>
      <label>City <input name="city" value="{city}" required></label>
      <label>Colonia <input name="colonia" value="{colonia}"></label>
      <label>State (Mexico) <input name="state" value="{state}" required placeholder="Baja California"></label>
      <label>Phone 1 <input name="phone1" value="{phone1}" required></label>
      <label>Phone 2 <input name="phone2" value="{phone2}"></label>
      <label>Email <input name="email" value="{email}" type="email"></label>
      <label>Emergency name <input name="emergencyfullname" value="{ename}" required></label>
      <label>Emergency phone <input name="emergencyphone" value="{ephone}" required></label>
      <label>Emergency email <input name="emergencyemail" value="{eemail}" type="email"></label>
      <button type="submit">{submit}</button>
    </form>
    <p class="muted">This form only updates patient demographics. Registering for a clinic is a separate action on the clinic page.</p>
    {script}
    "#,
        panel = panel,
        watch = watch,
        script = script,
        action = action,
        first = escape(&p.first),
        middle = escape(&p.middle),
        paternal = escape(&p.paternal_last),
        maternal = escape(&p.maternal_last),
        prefix = escape(&p.prefix),
        suffix = escape(&p.suffix),
        dob = escape(&p.dob),
        male = if p.gender == "Male" || p.gender == "m" {
            "selected"
        } else {
            ""
        },
        female = if p.gender == "Female" || p.gender == "f" {
            "selected"
        } else {
            ""
        },
        curp = escape(&p.curp),
        oldid = escape(&p.oldid),
        street1 = escape(&p.street1),
        street2 = escape(&p.street2),
        city = escape(&p.city),
        colonia = escape(&p.colonia),
        state = escape(&p.state),
        phone1 = escape(&p.phone1),
        phone2 = escape(&p.phone2),
        email = escape(&p.email),
        ename = escape(&p.emergencyfullname),
        ephone = escape(&p.emergencyphone),
        eemail = escape(&p.emergencyemail),
        submit = submit,
    )
}

/// Debounced live duplicate check (same search API as the tablet app).
const DUP_CHECK_SCRIPT: &str = r#"
<script>
(function () {
  const form = document.getElementById("patient-form");
  const panel = document.getElementById("dup-matches");
  if (!form || !panel || !form.hasAttribute("data-dup-watch")) return;
  const fields = ["first", "paternal_last", "maternal_last", "dob", "gender", "curp"];
  let timer = null;
  const run = () => {
    const params = new URLSearchParams();
    for (const name of fields) {
      const el = form.elements.namedItem(name);
      if (!el) continue;
      const v = (el.value || "").trim();
      if (v) params.set(name, v);
    }
    if (![...params.keys()].length) {
      panel.innerHTML = "";
      panel.className = "dup-panel";
      return;
    }
    panel.className = "dup-panel dup-loading";
    panel.innerHTML = "<p class=\"muted\">Checking for existing patients…</p>";
    fetch("/patients/match-check?" + params.toString(), { credentials: "same-origin" })
      .then((r) => r.text())
      .then((html) => {
        panel.className = "dup-panel";
        panel.innerHTML = html;
      })
      .catch(() => {
        panel.className = "dup-panel";
        panel.innerHTML = "";
      });
  };
  const schedule = () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(run, 400);
  };
  form.addEventListener("input", schedule);
  form.addEventListener("change", schedule);
  run();
})();
</script>
"#;

#[derive(Deserialize)]
pub struct PatientForm {
    first: String,
    middle: String,
    paternal_last: String,
    maternal_last: String,
    prefix: String,
    suffix: String,
    dob: String,
    gender: String,
    curp: String,
    oldid: String,
    street1: String,
    street2: String,
    city: String,
    colonia: String,
    state: String,
    phone1: String,
    phone2: String,
    email: String,
    emergencyfullname: String,
    emergencyphone: String,
    emergencyemail: String,
}

impl PatientForm {
    fn to_patient(&self) -> Patient {
        Patient {
            id: None,
            first: self.first.clone(),
            middle: self.middle.clone(),
            paternal_last: self.paternal_last.clone(),
            maternal_last: self.maternal_last.clone(),
            prefix: self.prefix.clone(),
            suffix: self.suffix.clone(),
            dob: self.dob.clone(),
            gender: self.gender.clone(),
            curp: self.curp.clone(),
            oldid: self.oldid.clone(),
            street1: self.street1.clone(),
            street2: self.street2.clone(),
            city: self.city.clone(),
            colonia: self.colonia.clone(),
            state: self.state.clone(),
            phone1: self.phone1.clone(),
            phone2: self.phone2.clone(),
            email: self.email.clone(),
            emergencyfullname: self.emergencyfullname.clone(),
            emergencyphone: self.emergencyphone.clone(),
            emergencyemail: self.emergencyemail.clone(),
        }
    }
}

#[derive(Debug, Deserialize, Default)]
pub struct MatchQuery {
    first: Option<String>,
    paternal_last: Option<String>,
    maternal_last: Option<String>,
    dob: Option<String>,
    gender: Option<String>,
    curp: Option<String>,
}

fn nonempty(s: &Option<String>) -> Option<String> {
    s.as_ref()
        .map(|v| v.trim().to_string())
        .filter(|v| !v.is_empty())
}

/// Build search query the same way the tablet registration app does.
fn match_search_query(q: &MatchQuery) -> Option<(Vec<(String, String)>, &'static str)> {
    let first = nonempty(&q.first);
    let paternal = nonempty(&q.paternal_last);
    let maternal = nonempty(&q.maternal_last);
    let dob = nonempty(&q.dob);
    let gender = nonempty(&q.gender);
    let curp = nonempty(&q.curp);

    // Exact match (tablet AppPatientInfoFragment.checkForExistingPatient).
    if first.is_some()
        && paternal.is_some()
        && maternal.is_some()
        && dob.is_some()
        && gender.is_some()
    {
        // Same fields as tablet AppPatientInfoFragment.checkForExistingPatient.
        let params = vec![
            ("paternal_last".into(), paternal.unwrap()),
            ("maternal_last".into(), maternal.unwrap()),
            ("first".into(), first.unwrap()),
            ("dob".into(), dob.unwrap()),
            ("gender".into(), gender.unwrap()),
            ("exact".into(), "true".into()),
        ];
        let _ = curp; // CURP checked via soft path when exact fields incomplete
        return Some((params, "exact"));
    }

    if let Some(c) = curp {
        if c.chars().count() >= 4 {
            return Some((
                vec![("curp".into(), c), ("exact".into(), "false".into())],
                "curp",
            ));
        }
    }

    // Soft name match while typing (like tablet short name search).
    if let (Some(f), Some(p)) = (first, paternal) {
        if f.chars().count() >= 2 && p.chars().count() >= 2 {
            let mut params = vec![
                ("first".into(), f),
                ("paternal_last".into(), p),
                ("exact".into(), "false".into()),
            ];
            if let Some(m) = maternal {
                if m.chars().count() >= 2 {
                    params.push(("maternal_last".into(), m));
                }
            }
            return Some((params, "similar"));
        }
    }

    None
}

async fn load_match_summaries(
    api: &TschartsClient,
    token: &str,
    ids: &[i64],
    limit: usize,
) -> Vec<(i64, Patient)> {
    let mut out = Vec::new();
    for id in ids.iter().take(limit) {
        if let Ok(p) = api.get_patient(token, *id).await {
            out.push((*id, p));
        } else {
            out.push((*id, Patient::default()));
        }
    }
    out
}

fn render_match_panel(kind: &str, matches: &[(i64, Patient)], total: usize) -> String {
    if matches.is_empty() {
        return r#"<p class="dup-ok">No matching patients found.</p>"#.into();
    }
    let title = match kind {
        "exact" => format!(
            "Possible duplicate: {total} exact match{} (same name, DOB, gender)",
            if total == 1 { "" } else { "es" }
        ),
        "curp" => format!(
            "{total} patient{} with similar CURP",
            if total == 1 { "" } else { "s" }
        ),
        _ => format!(
            "{total} similar patient{}",
            if total == 1 { "" } else { "s" }
        ),
    };
    let cls = if kind == "exact" {
        "dup-panel-inner dup-warn"
    } else {
        "dup-panel-inner dup-info"
    };
    let mut rows = String::new();
    for (id, p) in matches {
        let name = format!(
            "{} {} {}",
            p.first.trim(),
            p.paternal_last.trim(),
            p.maternal_last.trim()
        );
        rows.push_str(&format!(
            r#"<li>
              {avatar}
              <strong>#{id}</strong> {name}
              <span class="muted">· {dob} · {gender}</span>
              <a class="btn" href="/patients/{id}/edit">Open existing</a>
            </li>"#,
            avatar = headshot_img(*id, "sm", name.trim()),
            id = id,
            name = escape(name.trim()),
            dob = escape(&p.dob),
            gender = escape(&p.gender),
        ));
    }
    let more = if total > matches.len() {
        format!(
            r#"<p class="muted">Showing {shown} of {total}. <a href="/patients/search">Full search</a></p>"#,
            shown = matches.len(),
            total = total
        )
    } else {
        String::new()
    };
    format!(
        r#"<div class="{cls}">
      <p class="dup-title">{title}</p>
      <ul class="dup-list">{rows}</ul>
      {more}
      <p class="muted">If this is the same person, open the existing record instead of creating a new one.</p>
    </div>"#,
        cls = cls,
        title = escape(&title),
        rows = rows,
        more = more,
    )
}

/// Live / fragment endpoint used by the new-patient form.
pub async fn match_check(
    State(state): State<AppState>,
    session: Session,
    Query(q): Query<MatchQuery>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let Some((params, kind)) = match_search_query(&q) else {
        return Ok(Html(String::new()).into_response());
    };
    let qrefs: Vec<(&str, String)> = params
        .iter()
        .map(|(k, v)| (k.as_str(), v.clone()))
        .collect();
    let ids = state
        .api
        .search_patients(&token, &qrefs)
        .await
        .unwrap_or_default();
    let summaries = load_match_summaries(&state.api, &token, &ids, 8).await;
    Ok(Html(render_match_panel(kind, &summaries, ids.len())).into_response())
}

async fn find_exact_duplicates(
    api: &TschartsClient,
    token: &str,
    p: &Patient,
) -> anyhow::Result<Vec<(i64, Patient)>> {
    let q = MatchQuery {
        first: Some(p.first.clone()),
        paternal_last: Some(p.paternal_last.clone()),
        maternal_last: Some(p.maternal_last.clone()),
        dob: Some(p.dob.clone()),
        gender: Some(p.gender.clone()),
        curp: None,
    };
    let Some((params, _)) = match_search_query(&q) else {
        return Ok(vec![]);
    };
    let qrefs: Vec<(&str, String)> = params
        .iter()
        .map(|(k, v)| (k.as_str(), v.clone()))
        .collect();
    let ids = api.search_patients(token, &qrefs).await?;
    Ok(load_match_summaries(api, token, &ids, 12).await)
}

pub async fn new_form(session: Session) -> Result<Response, Response> {
    let _ = require_token(&session).await?;
    let body = format!(
        "<h1>New patient</h1><p class=\"muted\">As you enter name, DOB, and gender, we check for existing patients (same logic as the tablet registration app).</p>{}",
        patient_form_fields(&Patient::default(), "/patients/new", "Create patient", true)
    );
    Ok(layout("New patient", &body).into_response())
}

pub async fn create(
    State(state): State<AppState>,
    session: Session,
    Form(form): Form<PatientForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let patient = form.to_patient();

    // Tablet-style exact pre-check before create.
    let dups = find_exact_duplicates(&state.api, &token, &patient)
        .await
        .unwrap_or_default();
    if !dups.is_empty() {
        let panel = render_match_panel("exact", &dups, dups.len());
        return Ok(layout(
            "New patient",
            &format!(
                "{}{}{}",
                flash_err(
                    "An existing patient matches this name, DOB, and gender. Open that record instead of creating a duplicate."
                ),
                panel,
                patient_form_fields(&patient, "/patients/new", "Create patient", true)
            ),
        )
        .into_response());
    }

    match state.api.create_patient(&token, &patient).await {
        Ok(id) => Ok(layout(
            "Patient created",
            &format!(
                "{}<p>Patient id <strong>{id}</strong>. You can now register them on a clinic page.</p>
                 <p><a class=\"btn\" href=\"/patients/{id}/edit\">Edit / add headshot</a>
                 <a class=\"btn\" href=\"/clinics\">Clinics</a></p>",
                flash_ok("Patient created"),
                id = id
            ),
        )
        .into_response()),
        Err(e) => {
            let msg = e.to_string();
            // POST conflict key omits maternal_last; re-search that key for links.
            let mut panel = String::new();
            if msg.contains("already exists") {
                let q = [
                    ("paternal_last", patient.paternal_last.clone()),
                    ("first", patient.first.clone()),
                    ("dob", patient.dob.clone()),
                    ("gender", patient.gender.clone()),
                    ("exact", "true".into()),
                ];
                if let Ok(ids) = state.api.search_patients(&token, &q).await {
                    let summaries = load_match_summaries(&state.api, &token, &ids, 12).await;
                    panel = render_match_panel("exact", &summaries, ids.len());
                }
            }
            Ok(layout(
                "New patient",
                &format!(
                    "{}{}{}",
                    flash_err(&msg),
                    panel,
                    patient_form_fields(&patient, "/patients/new", "Create patient", true)
                ),
            )
            .into_response())
        }
    }
}

#[derive(Deserialize)]
pub struct EditQuery {
    #[serde(default)]
    msg: Option<String>,
    #[serde(default)]
    err: Option<String>,
}

pub async fn edit_form(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
    Query(q): Query<EditQuery>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let patient = state
        .api
        .get_patient(&token, id)
        .await
        .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?;
    let flash = q
        .msg
        .as_deref()
        .map(flash_ok)
        .or_else(|| q.err.as_deref().map(flash_err))
        .unwrap_or_default();
    let name = format!(
        "{} {} {}",
        patient.first, patient.paternal_last, patient.maternal_last
    );
    let photo = format!(
        r#"
    <section class="headshot-block">
      <h2>Headshot</h2>
      <div class="headshot-row">
        {img}
        <form class="headshot-upload" method="post" action="/patients/{id}/headshot" enctype="multipart/form-data">
          <label>Upload or replace photo
            <input type="file" name="photo" accept="image/*" required>
          </label>
          <button type="submit" class="btn">Save headshot</button>
          <p class="muted">Replaces any previous headshot for this patient.</p>
        </form>
      </div>
    </section>
    "#,
        img = headshot_img(id, "lg", name.trim()),
        id = id,
    );
    let form = patient_form_fields(
        &patient,
        &format!("/patients/{id}/edit"),
        "Save changes",
        false,
    );
    let body = format!(
        "<h1>Edit patient {id}</h1>{flash}{photo}{form}",
        id = id,
        flash = flash,
        photo = photo,
        form = form,
    );
    Ok(layout("Edit patient", &body).into_response())
}

pub async fn update(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
    Form(form): Form<PatientForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let patient = form.to_patient();
    match state.api.update_patient(&token, id, &patient).await {
        Ok(()) => Ok(Redirect::to(&format!("/patients/{id}/edit")).into_response()),
        Err(e) => Ok(layout(
            "Edit patient",
            &format!(
                "{}{}",
                flash_err(&e.to_string()),
                patient_form_fields(
                    &patient,
                    &format!("/patients/{id}/edit"),
                    "Save changes",
                    false
                )
            ),
        )
        .into_response()),
    }
}

pub async fn search_form(session: Session) -> Result<Response, Response> {
    let _ = require_token(&session).await?;
    let body = r#"
    <h1>Find patient</h1>
    <form method="post" action="/patients/search" class="stack">
      <label>Name (partial) <input name="name" placeholder="search any name field"></label>
      <label>Paternal last <input name="paternal_last"></label>
      <label>Maternal last <input name="maternal_last"></label>
      <label>First <input name="first"></label>
      <label>CURP <input name="curp"></label>
      <label><input type="checkbox" name="exact" value="true"> Exact match</label>
      <button type="submit">Search</button>
    </form>
    "#;
    Ok(layout("Find patient", body).into_response())
}

#[derive(Deserialize)]
pub struct SearchForm {
    name: Option<String>,
    paternal_last: Option<String>,
    maternal_last: Option<String>,
    first: Option<String>,
    curp: Option<String>,
    exact: Option<String>,
}

pub async fn search(
    State(state): State<AppState>,
    session: Session,
    Form(form): Form<SearchForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let mut q: Vec<(&str, String)> = Vec::new();
    if let Some(v) = form.name.filter(|s| !s.is_empty()) {
        q.push(("name", v));
    }
    if let Some(v) = form.paternal_last.filter(|s| !s.is_empty()) {
        q.push(("paternal_last", v));
    }
    if let Some(v) = form.maternal_last.filter(|s| !s.is_empty()) {
        q.push(("maternal_last", v));
    }
    if let Some(v) = form.first.filter(|s| !s.is_empty()) {
        q.push(("first", v));
    }
    if let Some(v) = form.curp.filter(|s| !s.is_empty()) {
        q.push(("curp", v));
    }
    if form.exact.as_deref() == Some("true") {
        q.push(("exact", "true".into()));
    }
    if q.is_empty() {
        return Ok(layout(
            "Find patient",
            &format!(
                "{}{}",
                flash_err("Enter at least one search field"),
                r#"<p><a href="/patients/search">Back</a></p>"#
            ),
        )
        .into_response());
    }

    let ids = state
        .api
        .search_patients(&token, &q)
        .await
        .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?;

    let mut rows = String::new();
    for id in &ids {
        let p = state.api.get_patient(&token, *id).await.unwrap_or_default();
        let name = format!("{} {} {}", p.first, p.paternal_last, p.maternal_last);
        rows.push_str(&format!(
            r#"<tr>
              <td class="photo-cell">{avatar}</td>
              <td>{id}</td>
              <td>{name}</td>
              <td>{dob}</td>
              <td><a class="btn" href="/patients/{id}/edit">Edit</a></td>
            </tr>"#,
            avatar = headshot_img(*id, "sm", name.trim()),
            id = id,
            name = escape(name.trim()),
            dob = escape(&p.dob),
        ));
    }

    let body = format!(
        r#"
    <h1>Search results</h1>
    <p><a href="/patients/search">New search</a></p>
    <table>
      <thead><tr><th></th><th>ID</th><th>Name</th><th>DOB</th><th></th></tr></thead>
      <tbody>{}</tbody>
    </table>
    "#,
        if rows.is_empty() {
            "<tr><td colspan=\"5\">No matches.</td></tr>".into()
        } else {
            rows
        }
    );
    Ok(layout("Search results", &body).into_response())
}
