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

use std::collections::{HashMap, HashSet};

use axum::extract::{Path, Query, State};
use axum::response::{IntoResponse, Redirect, Response};
use axum::Form;
use chrono::{Local, NaiveDate};
use futures::stream::{self, StreamExt};
use serde::Deserialize;
use tower_sessions::Session;

use crate::clinic_filter::{
    can_register, delete_allowed, filter_clinics, overlapping_clinics, Clinic,
    ClinicListMode, ClinicPhase,
};
use crate::avatar::headshot_img;
use crate::clinic_stats::{
    arrival_profile, compute_stats, gender_bucket, group_regs_by_day, is_return_patient,
    parse_timein, rank_performance, regs_in_clinic_window, ArrivalProfile, Busyness,
    ClinicStats, GenderBucket, PerformanceRanking, RatePace, StartTiming,
};
use crate::client::{format_mdy, format_weekday_mdy, Patient, Registration};
use crate::html::{escape, flash_err, flash_ok, layout};
use crate::session::require_token;
use crate::AppState;

#[derive(Deserialize)]
pub struct ListQuery {
    #[serde(default)]
    mode: Option<String>,
    from: Option<String>,
    to: Option<String>,
    #[serde(default)]
    msg: Option<String>,
    #[serde(default)]
    err: Option<String>,
}

pub async fn home() -> Redirect {
    Redirect::to("/clinics")
}

pub async fn list(
    State(state): State<AppState>,
    session: Session,
    Query(q): Query<ListQuery>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let all = state
        .api
        .list_clinics(&token)
        .await
        .map_err(|e| error_page(&e.to_string()))?;

    let mode_key = q.mode.as_deref().unwrap_or("default");
    let mode = match mode_key {
        "all_past" => ClinicListMode::AllPast,
        "future" => ClinicListMode::FutureOnly,
        "range" => {
            let from = q
                .from
                .as_deref()
                .and_then(|s| NaiveDate::parse_from_str(s, "%Y-%m-%d").ok())
                .unwrap_or(today - chrono::TimeDelta::days(365));
            let to = q
                .to
                .as_deref()
                .and_then(|s| NaiveDate::parse_from_str(s, "%Y-%m-%d").ok())
                .unwrap_or(today);
            ClinicListMode::DateRange { from, to }
        }
        _ => ClinicListMode::DefaultLastYear,
    };

    let clinics = filter_clinics(&all, mode, today);

    // Parallel in-window registration day + unique patient counts.
    let pairs: Vec<(i64, usize, usize)> = stream::iter(clinics.iter().cloned())
        .map(|c| {
            let api = state.api.clone();
            let token = token.clone();
            async move {
                let regs = api.list_enrollments(&token, c.id).await.unwrap_or_default();
                let in_window = regs_in_clinic_window(&c, &regs);
                let days = group_regs_by_day(&in_window).len();
                let unique = {
                    let mut seen = HashSet::new();
                    for r in &in_window {
                        seen.insert(r.patient);
                    }
                    seen.len()
                };
                (c.id, days, unique)
            }
        })
        .buffer_unordered(6)
        .collect()
        .await;
    let counts_by_id: HashMap<i64, (usize, usize)> = pairs
        .into_iter()
        .map(|(id, days, unique)| (id, (days, unique)))
        .collect();

    let mut rows = String::new();
    for c in &clinics {
        let phase = match c.phase_on(today) {
            ClinicPhase::Future => "future",
            ClinicPhase::Current => "current",
            ClinicPhase::Past => "past",
        };
        let (days, unique) = counts_by_id.get(&c.id).copied().unwrap_or((0, 0));
        let mut ops = format!(
            r#"<a class="btn" href="/clinics/{id}/stats">Stats</a>"#,
            id = c.id
        );
        if delete_allowed(c, today) {
            ops.push_str(&format!(
                r#" <a class="btn" href="/clinics/{id}/edit">Edit</a>
                <form class="inline" method="post" action="/clinics/{id}/delete" onsubmit="return confirm('Delete this future clinic?');">
                <button type="submit" class="btn danger">Delete</button></form>"#,
                id = c.id
            ));
        }
        rows.push_str(&format!(
            r#"<tr>
              <td><a href="/clinics/{id}">{id}</a></td>
              <td>{loc}</td>
              <td>{start}</td>
              <td>{end}</td>
              <td class="num">{days}</td>
              <td class="num">{unique}</td>
              <td><span class="badge {phase}">{phase}</span></td>
              <td class="actions">{ops}</td>
            </tr>"#,
            id = c.id,
            loc = escape(&c.place),
            start = format_mdy(c.start),
            end = format_mdy(c.end),
            days = days,
            unique = unique,
            phase = phase,
            ops = ops,
        ));
    }

    let flash = q
        .msg
        .as_deref()
        .map(flash_ok)
        .or_else(|| q.err.as_deref().map(flash_err))
        .unwrap_or_default();

    let selected = match mode_key {
        "all_past" | "future" | "range" => mode_key,
        _ => "default",
    };
    let btn = |mode: &str| {
        if mode == selected {
            "btn active"
        } else {
            "btn"
        }
    };
    let range_form_class = if selected == "range" {
        "range range-active"
    } else {
        "range"
    };

    let body = format!(
        r#"
    <h1>Clinics</h1>
    {flash}
    <p class="muted">Default view: past calendar year including any clinic currently running. Future clinics are hidden unless you select “Future”.</p>
    <div class="toolbar-row">
      <div class="toolbar filter-toolbar" role="group" aria-label="Clinic views">
        <a class="{btn_default}" href="/clinics?mode=default" aria-current="{cur_default}">Last year + current</a>
        <a class="{btn_past}" href="/clinics?mode=all_past" aria-current="{cur_past}">All past</a>
        <a class="{btn_future}" href="/clinics?mode=future" aria-current="{cur_future}">Future</a>
      </div>
      <div class="toolbar-actions">
        <a class="btn create-clinic" href="/clinics/new">Create future clinic</a>
      </div>
    </div>
    <form class="{range_form}" method="get" action="/clinics">
      <input type="hidden" name="mode" value="range">
      <label>From <input type="date" name="from" value="{from}"></label>
      <label>To <input type="date" name="to" value="{to}"></label>
      <button type="submit" class="{btn_range}">Apply range</button>
    </form>
    <table>
      <thead><tr><th>ID</th><th>Place</th><th>Start</th><th>End</th><th>Reg. days</th><th>Unique patients</th><th>Status</th><th></th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    "#,
        flash = flash,
        btn_default = btn("default"),
        btn_past = btn("all_past"),
        btn_future = btn("future"),
        btn_range = btn("range"),
        cur_default = if selected == "default" { "page" } else { "false" },
        cur_past = if selected == "all_past" { "page" } else { "false" },
        cur_future = if selected == "future" { "page" } else { "false" },
        range_form = range_form_class,
        from = q.from.unwrap_or_default(),
        to = q.to.unwrap_or_default(),
        rows = if rows.is_empty() {
            "<tr><td colspan=\"8\">No clinics match this filter.</td></tr>".into()
        } else {
            rows
        }
    );

    Ok(layout("Clinics", &body).into_response())
}

pub async fn new_form(session: Session) -> Result<Response, Response> {
    let _ = require_token(&session).await?;
    Ok(layout("New clinic", &clinic_form_html("Create future clinic", "/clinics/new", "Create", None)).into_response())
}

#[derive(Deserialize)]
pub struct ClinicForm {
    place: String,
    start: String, // YYYY-MM-DD from HTML date input
    end: String,
}

fn parse_html_date(s: &str) -> anyhow::Result<NaiveDate> {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").map_err(|e| anyhow::anyhow!("{e}"))
}

fn clinic_form_html(title: &str, action: &str, submit: &str, clinic: Option<&Clinic>) -> String {
    let place = clinic.map(|c| escape(&c.place)).unwrap_or_default();
    let start = clinic
        .map(|c| c.start.format("%Y-%m-%d").to_string())
        .unwrap_or_default();
    let end = clinic
        .map(|c| c.end.format("%Y-%m-%d").to_string())
        .unwrap_or_default();
    format!(
        r#"
    <h1>{title}</h1>
    <form method="post" action="{action}" class="stack">
      <label>Place <input name="place" required placeholder="Ensenada" value="{place}"></label>
      <label>Start <input name="start" type="date" required value="{start}"></label>
      <label>End <input name="end" type="date" required value="{end}"></label>
      <button type="submit">{submit}</button>
    </form>
    "#,
        title = escape(title),
        action = escape(action),
        place = place,
        start = escape(&start),
        end = escape(&end),
        submit = escape(submit),
    )
}

fn format_overlap_list(clinics: &[Clinic], today: NaiveDate) -> String {
    let mut list = String::new();
    for c in clinics {
        let phase = match c.phase_on(today) {
            ClinicPhase::Future => "future",
            ClinicPhase::Current => "current",
            ClinicPhase::Past => "past",
        };
        list.push_str(&format!(
            r#"<li>Clinic #{id} — {place} ({start} – {end}) <span class="badge {phase}">{phase}</span></li>"#,
            id = c.id,
            place = escape(&c.place),
            start = format_mdy(c.start),
            end = format_mdy(c.end),
            phase = phase,
        ));
    }
    list
}

/// Current (or past) overlap: hard error, no edit prompt.
fn current_overlap_error_page(overlaps: &[Clinic], today: NaiveDate) -> Response {
    let list = format_overlap_list(overlaps, today);
    let body = format!(
        r#"
    {err}
    <p>There is a current clinic in that date range. You cannot create another clinic that overlaps it.</p>
    <ul>{list}</ul>
    <p><a class="btn" href="/clinics/new">Back</a>
       <a class="btn" href="/clinics">Clinics</a></p>
    {form}
    "#,
        err = flash_err("There is a current clinic in that date range."),
        list = list,
        form = clinic_form_html("Create future clinic", "/clinics/new", "Create", None),
    );
    layout("Clinic date conflict", &body).into_response()
}

/// Future overlap: ask whether to edit name / start / end (do not open clinic detail).
fn future_overlap_edit_prompt(overlaps: &[Clinic], today: NaiveDate) -> Response {
    let primary = &overlaps[0];
    let edit_href = format!("/clinics/{}/edit", primary.id);
    let confirm_plain = format!(
        "There is already a future clinic in that date range.\n\nClinic #{} — {} ({} – {}).\n\nDo you want to edit its name, start date, and end date?",
        primary.id,
        primary.place,
        format_mdy(primary.start),
        format_mdy(primary.end),
    );
    let confirm_js = serde_json::to_string(&confirm_plain).unwrap_or_else(|_| {
        "\"There is already a future clinic in that date range.\"".into()
    });
    let edit_href_js = serde_json::to_string(&edit_href).unwrap_or_else(|_| "\"/clinics\"".into());
    let list = format_overlap_list(overlaps, today);
    let body = format!(
        r#"
    <h1>Create future clinic</h1>
    <p class="flash warn">There is already a future clinic in that date range.</p>
    <p>Do you want to edit its name, start date, and end date?</p>
    <ul>{list}</ul>
    <div class="actions">
      <a class="btn primary" href="{edit_href}">Yes, edit name and dates</a>
      <a class="btn" href="/clinics/new">No, go back</a>
    </div>
    <script>
      (function () {{
        if (window.confirm({confirm_js})) {{
          window.location.href = {edit_href_js};
        }}
      }})();
    </script>
    "#,
        list = list,
        edit_href = escape(&edit_href),
        confirm_js = confirm_js,
        edit_href_js = edit_href_js,
    );
    layout("Clinic already exists", &body).into_response()
}

pub async fn create(
    State(state): State<AppState>,
    session: Session,
    Form(form): Form<ClinicForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let start_d = parse_html_date(&form.start).map_err(|e| error_page(&e.to_string()))?;
    let end_d = parse_html_date(&form.end).map_err(|e| error_page(&e.to_string()))?;
    if end_d < start_d {
        return Ok(layout(
            "New clinic",
            &format!(
                "{}{}",
                flash_err("End date must be on or after start date."),
                clinic_form_html("Create future clinic", "/clinics/new", "Create", None)
            ),
        )
        .into_response());
    }
    if start_d <= today {
        return Ok(layout(
            "New clinic",
            &format!(
                "{}{}",
                flash_err("Only future clinics can be created (start date must be after today)."),
                clinic_form_html("Create future clinic", "/clinics/new", "Create", None)
            ),
        )
        .into_response());
    }

    let all = state
        .api
        .list_clinics(&token)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    let overlaps = overlapping_clinics(&all, start_d, end_d, None);
    if !overlaps.is_empty() {
        let current: Vec<Clinic> = overlaps
            .iter()
            .filter(|c| c.phase_on(today) == ClinicPhase::Current)
            .cloned()
            .collect();
        if !current.is_empty() {
            return Ok(current_overlap_error_page(&current, today));
        }
        let future: Vec<Clinic> = overlaps
            .iter()
            .filter(|c| c.phase_on(today) == ClinicPhase::Future)
            .cloned()
            .collect();
        if !future.is_empty() {
            return Ok(future_overlap_edit_prompt(&future, today));
        }
        // Past-only overlap (unexpected for a future create range): treat as error.
        return Ok(layout(
            "New clinic",
            &format!(
                "{}{}",
                flash_err("There is already a clinic in that date range."),
                clinic_form_html("Create future clinic", "/clinics/new", "Create", None)
            ),
        )
        .into_response());
    }

    let start = format_mdy(start_d);
    let end = format_mdy(end_d);
    match state
        .api
        .create_clinic(&token, &form.place, &start, &end)
        .await
    {
        Ok(id) => Ok(Redirect::to(&format!("/clinics?mode=future&msg=Created%20clinic%20{id}")).into_response()),
        Err(e) => Ok(layout(
            "New clinic",
            &format!(
                "{}{}",
                flash_err(&e.to_string()),
                clinic_form_html("Create future clinic", "/clinics/new", "Create", None)
            ),
        )
        .into_response()),
    }
}

pub async fn edit_form(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let clinic = state
        .api
        .get_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    if clinic.phase_on(today) != ClinicPhase::Future {
        return Ok(Redirect::to(&format!(
            "/clinics/{id}?err=Only%20future%20clinics%20can%20be%20edited"
        ))
        .into_response());
    }
    let body = clinic_form_html(
        &format!("Edit future clinic {id}"),
        &format!("/clinics/{id}/edit"),
        "Save changes",
        Some(&clinic),
    );
    Ok(layout("Edit clinic", &body).into_response())
}

pub async fn update(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
    Form(form): Form<ClinicForm>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let existing = state
        .api
        .get_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    if existing.phase_on(today) != ClinicPhase::Future {
        return Ok(Redirect::to(&format!(
            "/clinics/{id}?err=Only%20future%20clinics%20can%20be%20edited"
        ))
        .into_response());
    }
    let start_d = parse_html_date(&form.start).map_err(|e| error_page(&e.to_string()))?;
    let end_d = parse_html_date(&form.end).map_err(|e| error_page(&e.to_string()))?;
    if end_d < start_d {
        return Ok(layout(
            "Edit clinic",
            &format!(
                "{}{}",
                flash_err("End date must be on or after start date."),
                clinic_form_html(
                    &format!("Edit future clinic {id}"),
                    &format!("/clinics/{id}/edit"),
                    "Save changes",
                    Some(&existing),
                )
            ),
        )
        .into_response());
    }
    if start_d <= today {
        return Ok(layout(
            "Edit clinic",
            &format!(
                "{}{}",
                flash_err("Edited clinic must remain in the future (start after today)."),
                clinic_form_html(
                    &format!("Edit future clinic {id}"),
                    &format!("/clinics/{id}/edit"),
                    "Save changes",
                    Some(&existing),
                )
            ),
        )
        .into_response());
    }

    let all = state
        .api
        .list_clinics(&token)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    let overlaps = overlapping_clinics(&all, start_d, end_d, Some(id));
    if !overlaps.is_empty() {
        let other = &overlaps[0];
        return Ok(layout(
            "Edit clinic",
            &format!(
                "{}{}",
                flash_err(&format!(
                    "There is already a clinic on that date: #{} {} ({} – {}).",
                    other.id,
                    other.place,
                    format_mdy(other.start),
                    format_mdy(other.end)
                )),
                clinic_form_html(
                    &format!("Edit future clinic {id}"),
                    &format!("/clinics/{id}/edit"),
                    "Save changes",
                    Some(&existing),
                )
            ),
        )
        .into_response());
    }

    let start = format_mdy(start_d);
    let end = format_mdy(end_d);
    match state
        .api
        .update_clinic(&token, id, &form.place, &start, &end)
        .await
    {
        Ok(()) => Ok(Redirect::to(&format!("/clinics/{id}?msg=Clinic%20updated")).into_response()),
        Err(e) => Ok(layout(
            "Edit clinic",
            &format!(
                "{}{}",
                flash_err(&e.to_string()),
                clinic_form_html(
                    &format!("Edit future clinic {id}"),
                    &format!("/clinics/{id}/edit"),
                    "Save changes",
                    Some(&existing),
                )
            ),
        )
        .into_response()),
    }
}

pub async fn delete(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let clinic = state
        .api
        .get_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    if !delete_allowed(&clinic, today) {
        return Ok(Redirect::to("/clinics?err=Only%20future%20clinics%20can%20be%20deleted").into_response());
    }
    state
        .api
        .delete_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    Ok(Redirect::to("/clinics?mode=future&msg=Deleted").into_response())
}

pub async fn stats(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let clinic = state
        .api
        .get_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    let all_regs = state
        .api
        .list_enrollments(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    // Drop enrollments made outside the clinic calendar (e.g. dashboard
    // registrations between clinics) — they are not clinic-day performance.
    let regs = regs_in_clinic_window(&clinic, &all_regs);
    let excluded_outside = all_regs.len().saturating_sub(regs.len());

    let all_clinics = state
        .api
        .list_clinics(&token)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    let clinic_start_by_id: HashMap<i64, NaiveDate> =
        all_clinics.iter().map(|c| (c.id, c.start)).collect();

    let mut patient_ids: Vec<i64> = regs.iter().map(|r| r.patient).collect();
    patient_ids.sort_unstable();
    patient_ids.dedup();

    let patients: Vec<(i64, Patient)> = stream::iter(patient_ids.clone())
        .map(|pid| {
            let api = state.api.clone();
            let token = token.clone();
            async move {
                let p = api.get_patient(&token, pid).await.unwrap_or_default();
                (pid, p)
            }
        })
        .buffer_unordered(8)
        .collect()
        .await;

    let prior_flags: Vec<(i64, bool)> = stream::iter(patient_ids.clone())
        .map(|pid| {
            let api = state.api.clone();
            let token = token.clone();
            let clinic = clinic.clone();
            let clinic_start_by_id = clinic_start_by_id.clone();
            async move {
                let hist = api
                    .list_enrollments_for_patient(&token, pid)
                    .await
                    .unwrap_or_default();
                (pid, is_return_patient(&hist, &clinic, &clinic_start_by_id))
            }
        })
        .buffer_unordered(8)
        .collect()
        .await;
    let prior_patient_ids: HashSet<i64> = prior_flags
        .into_iter()
        .filter_map(|(pid, is_ret)| is_ret.then_some(pid))
        .collect();

    // Peer clinic-days (past + current): each in-window registration day is a ranking unit.
    let today = Local::now().date_naive();
    let compare_clinics: Vec<Clinic> = all_clinics
        .into_iter()
        .filter(|c| c.phase_on(today) != ClinicPhase::Future)
        .collect();
    let peer_day_chunks: Vec<Vec<ArrivalProfile>> = stream::iter(compare_clinics)
        .map(|c| {
            let api = state.api.clone();
            let token = token.clone();
            async move {
                let regs = api.list_enrollments(&token, c.id).await.unwrap_or_default();
                let in_window = regs_in_clinic_window(&c, &regs);
                group_regs_by_day(&in_window)
                    .into_iter()
                    .map(|(_day, day_regs)| arrival_profile(c.id, &day_regs))
                    .collect::<Vec<_>>()
            }
        })
        .buffer_unordered(6)
        .collect()
        .await;
    let mut peer_day_profiles: Vec<ArrivalProfile> =
        peer_day_chunks.into_iter().flatten().collect();

    // Prefer this clinic's already-loaded in-window regs for its own day profiles.
    peer_day_profiles.retain(|p| p.clinic_id != id);
    let by_day = group_regs_by_day(&regs);
    for (_day, day_regs) in &by_day {
        peer_day_profiles.push(arrival_profile(id, day_regs));
    }

    let day_entries: Vec<(NaiveDate, Vec<Registration>)> = by_day.into_iter().collect();
    let default_tab = day_entries
        .iter()
        .position(|(d, _)| *d == today)
        .or_else(|| day_entries.len().checked_sub(1))
        .unwrap_or(0);

    let mut tabs = String::new();
    let mut panels = String::new();
    for (idx, (day, day_regs)) in day_entries.iter().enumerate() {
        let s = compute_stats(&clinic, day_regs, &patients, &prior_patient_ids);
        let profile = arrival_profile(id, day_regs);
        let ranking = rank_performance(&profile, &peer_day_profiles);
        let selected = idx == default_tab;
        let label = format_weekday_mdy(*day);
        tabs.push_str(&format!(
            r#"<button type="button" class="day-tab{active}" role="tab" aria-selected="{sel}" aria-controls="stats-panel-{idx}" id="stats-tab-{idx}" data-day-tab="{idx}">{label} <span class="day-tab-count">{n}</span></button>"#,
            active = if selected { " active" } else { "" },
            sel = if selected { "true" } else { "false" },
            idx = idx,
            label = escape(&label),
            n = day_regs.len(),
        ));
        panels.push_str(&format!(
            r#"<div class="day-panel{hidden}" role="tabpanel" id="stats-panel-{idx}" aria-labelledby="stats-tab-{idx}" data-day-panel="{idx}"{hidden_attr}>
      {body}
    </div>"#,
            hidden = if selected { "" } else { " is-hidden" },
            hidden_attr = if selected { "" } else { " hidden" },
            idx = idx,
            body = render_stats_body(
                &s,
                &render_performance_ranking(&ranking, "clinic days", "clinic day"),
            ),
        ));
    }

    let stats_section = if day_entries.is_empty() {
        let s = compute_stats(&clinic, &regs, &patients, &prior_patient_ids);
        let ranking = rank_performance(&arrival_profile(id, &regs), &peer_day_profiles);
        render_stats_body(
            &s,
            &render_performance_ranking(&ranking, "clinic days", "clinic day"),
        )
    } else if day_entries.len() == 1 {
        panels
    } else {
        format!(
            r#"<div class="day-tabs" role="tablist" aria-label="Clinic days">{tabs}</div>
    {panels}
    <script>
    (() => {{
      const tabs = Array.from(document.querySelectorAll("[data-day-tab]"));
      const panels = Array.from(document.querySelectorAll("[data-day-panel]"));
      function activate(idx) {{
        tabs.forEach((t) => {{
          const on = t.getAttribute("data-day-tab") === String(idx);
          t.classList.toggle("active", on);
          t.setAttribute("aria-selected", on ? "true" : "false");
        }});
        panels.forEach((p) => {{
          const on = p.getAttribute("data-day-panel") === String(idx);
          p.classList.toggle("is-hidden", !on);
          if (on) p.removeAttribute("hidden"); else p.setAttribute("hidden", "");
        }});
      }}
      tabs.forEach((t) => t.addEventListener("click", () => activate(t.getAttribute("data-day-tab"))));
    }})();
    </script>"#,
            tabs = tabs,
            panels = panels
        )
    };

    let excluded_note = if excluded_outside > 0 {
        format!(
            r#"<p class="flash warn">{n} enrollment{s} outside {start}–{end} were excluded (e.g. registrations made between clinics).</p>"#,
            n = excluded_outside,
            s = if excluded_outside == 1 { "" } else { "s" },
            start = escape(&format_mdy(clinic.start)),
            end = escape(&format_mdy(clinic.end)),
        )
    } else {
        String::new()
    };

    let body = format!(
        r#"
    <h1>Clinic {id} statistics</h1>
    <p class="muted">{place} · {start} → {end}</p>
    <p class="muted">Ranking and stats use check-ins on clinic calendar days only. Empty setup/teardown days are omitted. Each day is compared with other clinic days.</p>
    {excluded_note}
    <div class="toolbar">
      <a class="btn" href="/clinics/{id}">Registered patients</a>
      <a class="btn" href="/clinics">Back to clinics</a>
    </div>
    {stats_section}
    "#,
        id = id,
        place = escape(&clinic.place),
        start = format_mdy(clinic.start),
        end = format_mdy(clinic.end),
        excluded_note = excluded_note,
        stats_section = stats_section,
    );

    Ok(layout("Clinic stats", &body).into_response())
}

fn render_arrival_hist(s: &ClinicStats) -> String {
    let max_hour = s
        .arrival_by_hour
        .iter()
        .map(|b| b.count)
        .max()
        .unwrap_or(1)
        .max(1);
    if s.arrival_by_hour.is_empty() {
        return r#"<p class="muted">No arrival times available.</p>"#.into();
    }
    let mut hist = String::from(
        r#"<div class="hist" role="img" aria-label="Arrival time histogram">"#,
    );
    for b in &s.arrival_by_hour {
        let pct = (b.count as f64 / max_hour as f64 * 100.0).round() as u32;
        hist.push_str(&format!(
            r#"<div class="hist-row">
              <span class="hist-label">{h:02}:00</span>
              <div class="hist-track"><div class="hist-bar" style="width:{pct}%"></div></div>
              <span class="hist-n">{n}</span>
            </div>"#,
            h = b.hour,
            pct = pct,
            n = b.count,
        ));
    }
    hist.push_str("</div>");
    hist
}

fn render_stats_body(s: &ClinicStats, ranking_html: &str) -> String {
    let age_range = match (s.age_min, s.age_max) {
        (Some(lo), Some(hi)) => format!("{lo} – {hi} years"),
        _ => "n/a".into(),
    };
    let age_avg = s
        .age_avg
        .map(|a| format!("{a:.1} years"))
        .unwrap_or_else(|| "n/a".into());
    let hist = render_arrival_hist(s);
    let max_nr = s.new_patients.max(s.return_patients).max(1);
    let new_pct = (s.new_patients as f64 / max_nr as f64 * 100.0).round() as u32;
    let ret_pct = (s.return_patients as f64 / max_nr as f64 * 100.0).round() as u32;

    format!(
        r#"{ranking_html}
    <section class="stats-grid">
      <div class="stat">
        <h2>Check-ins</h2>
        <p class="stat-value">{registered}</p>
        <p class="muted">Registration rows for this day</p>
      </div>
      <div class="stat">
        <h2>Age range</h2>
        <p class="stat-value">{age_range}</p>
        <p class="muted">Based on {with_dob} unique patients with DOB</p>
      </div>
      <div class="stat">
        <h2>Average age</h2>
        <p class="stat-value">{age_avg}</p>
      </div>
      <div class="stat">
        <h2>Boys / girls</h2>
        <p class="stat-value">{boys} / {girls}</p>
        <p class="muted">{unknown} unknown · unique patients</p>
      </div>
      <div class="stat">
        <h2>New vs return</h2>
        <p class="stat-value">{new_n} new · {ret_n} return</p>
        <p class="muted">Return = registered at an earlier clinic</p>
        <div class="hist compact">
          <div class="hist-row">
            <span class="hist-label">New</span>
            <div class="hist-track"><div class="hist-bar new" style="width:{new_pct}%"></div></div>
            <span class="hist-n">{new_n}</span>
          </div>
          <div class="hist-row">
            <span class="hist-label">Return</span>
            <div class="hist-track"><div class="hist-bar ret" style="width:{ret_pct}%"></div></div>
            <span class="hist-n">{ret_n}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="stats-block">
      <h2>Arrival times</h2>
      <p class="muted">{arrivals} of {registered} registrations have a parseable check-in time (hour of day).</p>
      {hist}
    </section>"#,
        ranking_html = ranking_html,
        registered = s.registered,
        age_range = escape(&age_range),
        with_dob = s.with_dob,
        age_avg = escape(&age_avg),
        boys = s.boys,
        girls = s.girls,
        unknown = s.gender_unknown,
        new_n = s.new_patients,
        ret_n = s.return_patients,
        new_pct = new_pct,
        ret_pct = ret_pct,
        arrivals = s.arrivals_parsed,
        hist = hist,
    )
}

fn render_performance_ranking(r: &PerformanceRanking, peer_plural: &str, peer_singular: &str) -> String {
    if r.peers_all < 3 {
        return format!(
            r#"
    <section class="stats-block rank-block">
      <h2>Performance ranking</h2>
      <p class="muted">Need at least 3 {peer_plural} with check-in times to rank volume, start time, and rate. Currently {n} comparable {unit}.</p>
    </section>
    "#,
            peer_plural = escape(peer_plural),
            n = r.peers_all,
            unit = if r.peers_all == 1 {
                escape(peer_singular)
            } else {
                escape(peer_plural)
            },
        );
    }

    let busy = match r.busyness {
        Some(Busyness::Busy) => (
            "Busy",
            "rank-high",
            "Peak hour was in the top third of clinic days",
        ),
        Some(Busyness::Moderate) => (
            "Moderate",
            "rank-mid",
            "Peak hour was typical versus other clinic days",
        ),
        Some(Busyness::Slow) => (
            "Slow",
            "rank-low",
            "Peak hour was in the bottom third of clinic days",
        ),
        None => ("n/a", "rank-na", "Not enough histogram data"),
    };
    let start = match r.start_timing {
        Some(StartTiming::Earlier) => (
            "Earlier than usual",
            "rank-high",
            "First check-in was earlier than most clinic days",
        ),
        Some(StartTiming::Average) => (
            "Average start",
            "rank-mid",
            "First check-in was near the usual time",
        ),
        Some(StartTiming::Later) => (
            "Later than usual",
            "rank-low",
            "First check-in was later than most clinic days",
        ),
        None => ("n/a", "rank-na", "Not enough start-time data"),
    };
    let rate = match r.rate_pace {
        Some(RatePace::Faster) => (
            "Faster than similar days",
            "rank-high",
            "Check-ins per hour were in the top third for similar-sized clinic days",
        ),
        Some(RatePace::Normal) => (
            "Normal rate",
            "rank-mid",
            "Check-ins per hour were typical for similar-sized clinic days",
        ),
        Some(RatePace::Slower) => (
            "Slower than similar days",
            "rank-low",
            "Check-ins per hour were in the bottom third for similar-sized clinic days",
        ),
        None => (
            "n/a",
            "rank-na",
            "Need more similarly sized clinic days with timing data",
        ),
    };

    let peak_med = r
        .median_peak
        .map(|v| format!("{v:.0}"))
        .unwrap_or_else(|| "n/a".into());
    let this_first = r.this_first_label.clone().unwrap_or_else(|| "n/a".into());
    let med_first = r.median_first_label.clone().unwrap_or_else(|| "n/a".into());
    let this_rate = r
        .this_rate
        .map(|v| format!("{v:.1}/hr"))
        .unwrap_or_else(|| "n/a".into());
    let med_rate = r
        .median_similar_rate
        .map(|v| format!("{v:.1}/hr"))
        .unwrap_or_else(|| "n/a".into());

    let (grade_label, grade_smile, grade_cls) = match r.overall {
        Some(g) => (g.label(), g.smiley(), g.css_class()),
        None => ("n/a", "❔", "grade-na"),
    };

    format!(
        r#"
    <section class="stats-block rank-block">
      <h2>Performance ranking</h2>
      <div class="overall-grade {grade_cls}">
        <span class="overall-smile" aria-hidden="true">{grade_smile}</span>
        <span class="overall-label">{grade_label}</span>
      </div>
      <p class="muted">Compared with {peers} {peer_plural} that have registration timestamps (terciles). Rate uses {similar} {peer_plural} with {lo}–{hi} check-ins. Grade blends volume, start time, and registration rate.</p>
      <div class="stats-grid rank-grid">
        <div class="stat">
          <h2>Volume</h2>
          <p class="stat-value"><span class="rank-pill {busy_cls}">{busy_label}</span></p>
          <p class="muted">{busy_help}</p>
          <p class="muted">Peak hour: {this_peak} check-ins (median {peak_med})</p>
        </div>
        <div class="stat">
          <h2>Registration start</h2>
          <p class="stat-value"><span class="rank-pill {start_cls}">{start_label}</span></p>
          <p class="muted">{start_help}</p>
          <p class="muted">First check-in: {this_first} (median {med_first})</p>
        </div>
        <div class="stat">
          <h2>Registration rate</h2>
          <p class="stat-value"><span class="rank-pill {rate_cls}">{rate_label}</span></p>
          <p class="muted">{rate_help}</p>
          <p class="muted">This day: {this_rate} · similar median: {med_rate}</p>
        </div>
      </div>
    </section>
    "#,
        grade_cls = grade_cls,
        grade_smile = grade_smile,
        grade_label = escape(grade_label),
        peers = r.peers_all,
        peer_plural = escape(peer_plural),
        similar = r.peers_similar,
        lo = r.similar_size_lo,
        hi = r.similar_size_hi,
        busy_label = busy.0,
        busy_cls = busy.1,
        busy_help = busy.2,
        this_peak = r.this_peak,
        peak_med = peak_med,
        start_label = start.0,
        start_cls = start.1,
        start_help = start.2,
        this_first = escape(&this_first),
        med_first = escape(&med_first),
        rate_label = rate.0,
        rate_cls = rate.1,
        rate_help = rate.2,
        this_rate = escape(&this_rate),
        med_rate = escape(&med_rate),
    )
}

pub async fn detail(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
    Query(q): Query<ListQuery>,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;
    let today = Local::now().date_naive();
    let clinic = state
        .api
        .get_clinic(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;
    let mut all_regs = state
        .api
        .list_enrollments(&token, id)
        .await
        .map_err(|e| error_page(&e.to_string()))?;

    // Stable order: check-in time, then registration id.
    all_regs.sort_by(|a, b| {
        let ta = a.timein.as_deref().and_then(parse_timein);
        let tb = b.timein.as_deref().and_then(parse_timein);
        ta.cmp(&tb).then_with(|| a.id.cmp(&b.id))
    });
    let regs = regs_in_clinic_window(&clinic, &all_regs);
    let outside_regs: Vec<&Registration> = all_regs
        .iter()
        .filter(|r| !regs.iter().any(|w| w.id == r.id))
        .collect();

    let allow_enroll = can_register(&clinic, today);

    let patient_ids: Vec<i64> = {
        let mut seen = HashSet::new();
        // Load demographics for in-window and outside rows (ops still need names).
        all_regs
            .iter()
            .filter_map(|r| seen.insert(r.patient).then_some(r.patient))
            .collect()
    };
    let mut patients: HashMap<i64, Patient> = HashMap::new();
    for pid in &patient_ids {
        let patient = match state.api.get_patient(&token, *pid).await {
            Ok(p) => p,
            Err(e) => {
                eprintln!("get_patient {pid}: {e:#}");
                Patient {
                    id: Some(*pid),
                    first: format!("(load failed: {e})"),
                    ..Patient::default()
                }
            }
        };
        patients.insert(*pid, patient);
    }

    let unique_in_window: HashSet<i64> = regs.iter().map(|r| r.patient).collect();
    let unique_patients = unique_in_window.len();
    let mut boys = 0usize;
    let mut girls = 0usize;
    let mut gender_unknown = 0usize;
    for pid in &unique_in_window {
        let gender = patients.get(pid).map(|p| p.gender.as_str()).unwrap_or("");
        match gender_bucket(gender) {
            GenderBucket::Male => boys += 1,
            GenderBucket::Female => girls += 1,
            GenderBucket::Unknown => gender_unknown += 1,
        }
    }

    // Group in-window registrations by check-in calendar day.
    let mut by_day: std::collections::BTreeMap<NaiveDate, Vec<&Registration>> =
        std::collections::BTreeMap::new();
    for r in &regs {
        if let Some(dt) = r.timein.as_deref().and_then(parse_timein) {
            by_day.entry(dt.date()).or_default().push(r);
        }
    }

    let day_keys: Vec<Option<NaiveDate>> = by_day.keys().copied().map(Some).collect();

    let default_tab = day_keys
        .iter()
        .position(|d| *d == Some(today))
        .or_else(|| day_keys.iter().rposition(|d| d.is_some()))
        .unwrap_or(0);

    let mut tabs = String::new();
    let mut panels = String::new();
    for (idx, day) in day_keys.iter().enumerate() {
        let day_regs: &[&Registration] = match day {
            Some(d) => by_day.get(d).map(|v| v.as_slice()).unwrap_or(&[]),
            None => &[],
        };
        let day_unique = {
            let mut s = HashSet::new();
            for r in day_regs {
                s.insert(r.patient);
            }
            s.len()
        };
        let label = match day {
            Some(d) => format_weekday_mdy(*d),
            None => "Unknown date".into(),
        };
        let selected = idx == default_tab;
        tabs.push_str(&format!(
            r#"<button type="button" class="day-tab{active}" role="tab" aria-selected="{sel}" aria-controls="day-panel-{idx}" id="day-tab-{idx}" data-day-tab="{idx}">{label} <span class="day-tab-count">{n}</span></button>"#,
            active = if selected { " active" } else { "" },
            sel = if selected { "true" } else { "false" },
            idx = idx,
            label = escape(&label),
            n = day_regs.len(),
        ));

        let mut rows = String::new();
        for r in day_regs {
            let patient = patients.get(&r.patient).cloned().unwrap_or_else(|| Patient {
                id: Some(r.patient),
                first: "(missing)".into(),
                ..Patient::default()
            });
            let name = format!(
                "{} {} {}",
                patient.first, patient.paternal_last, patient.maternal_last
            );
            let time_label = r
                .timein
                .as_deref()
                .and_then(parse_timein)
                .map(|dt| dt.format("%H:%M").to_string())
                .unwrap_or_else(|| "—".into());
            rows.push_str(&format!(
                r#"<tr>
              <td class="photo-cell">{avatar}</td>
              <td>{pid}</td>
              <td>{name}</td>
              <td class="num">{time}</td>
              <td>{dob}</td>
              <td>{gender}</td>
              <td>{curp}</td>
              <td class="actions">
                <a class="btn" href="/patients/{pid}/edit">Edit</a>
                <a class="btn" href="/imaging/clinic/{cid}/patient/{pid}">X-rays</a>
                <form class="inline" method="post" action="/clinics/{cid}/unregister/{rid}" onsubmit="return confirm('Unregister this patient?');">
                  <button type="submit" class="btn danger">Unregister</button>
                </form>
              </td>
            </tr>"#,
                avatar = headshot_img(r.patient, "sm", name.trim()),
                pid = r.patient,
                name = escape(name.trim()),
                time = escape(&time_label),
                dob = escape(&patient.dob),
                gender = escape(&patient.gender),
                curp = curp_cell(&patient.curp),
                cid = id,
                rid = r.id,
            ));
        }
        if rows.is_empty() {
            rows = r#"<tr><td colspan="8">No check-ins this day.</td></tr>"#.into();
        }
        panels.push_str(&format!(
            r#"<div class="day-panel{hidden}" role="tabpanel" id="day-panel-{idx}" aria-labelledby="day-tab-{idx}" data-day-panel="{idx}"{hidden_attr}>
      <p class="muted">{checkins} check-in{checkins_s} · {unique} unique patient{unique_s}</p>
      <table>
        <thead><tr><th></th><th>Patient ID</th><th>Name</th><th>Time</th><th>DOB</th><th>Gender</th><th>CURP</th><th></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"#,
            hidden = if selected { "" } else { " is-hidden" },
            hidden_attr = if selected {
                ""
            } else {
                " hidden"
            },
            idx = idx,
            checkins = day_regs.len(),
            checkins_s = if day_regs.len() == 1 { "" } else { "s" },
            unique = day_unique,
            unique_s = if day_unique == 1 { "" } else { "s" },
            rows = rows,
        ));
    }

    let day_section = if regs.is_empty() {
        r#"<h2>Registered patients</h2>
    <table>
      <thead><tr><th></th><th>Patient ID</th><th>Name</th><th>Time</th><th>DOB</th><th>Gender</th><th>CURP</th><th></th></tr></thead>
      <tbody><tr><td colspan="8">No patients registered.</td></tr></tbody>
    </table>"#
            .into()
    } else if day_keys.len() <= 1 {
        // Single day: no tab chrome.
        format!(
            r#"<h2>Registered patients</h2>
    {panels}"#,
            panels = panels
        )
    } else {
        format!(
            r#"<h2>Registered patients by day</h2>
    <div class="day-tabs" role="tablist" aria-label="Clinic days">{tabs}</div>
    {panels}
    <script>
    (() => {{
      const tabs = Array.from(document.querySelectorAll("[data-day-tab]"));
      const panels = Array.from(document.querySelectorAll("[data-day-panel]"));
      function activate(idx) {{
        tabs.forEach((t) => {{
          const on = t.getAttribute("data-day-tab") === String(idx);
          t.classList.toggle("active", on);
          t.setAttribute("aria-selected", on ? "true" : "false");
        }});
        panels.forEach((p) => {{
          const on = p.getAttribute("data-day-panel") === String(idx);
          p.classList.toggle("is-hidden", !on);
          if (on) p.removeAttribute("hidden"); else p.setAttribute("hidden", "");
        }});
      }}
      tabs.forEach((t) => t.addEventListener("click", () => activate(t.getAttribute("data-day-tab"))));
    }})();
    </script>"#,
            tabs = tabs,
            panels = panels
        )
    };

    let register_link = if allow_enroll {
        format!(r#"<a class="btn primary" href="/clinics/{id}/register">Register patient</a>"#)
    } else {
        r#"<span class="muted">Enroll disabled for future clinics.</span>"#.into()
    };

    let flash = q
        .msg
        .as_deref()
        .map(flash_ok)
        .or_else(|| q.err.as_deref().map(flash_err))
        .unwrap_or_default();

    let loc = if clinic.place.trim().is_empty() {
        "Unknown location".into()
    } else {
        clinic.place.clone()
    };
    let dates = if clinic.start == clinic.end {
        format_mdy(clinic.start)
    } else {
        format!("{} – {}", format_mdy(clinic.start), format_mdy(clinic.end))
    };
    let boys_girls = if gender_unknown > 0 {
        format!("{boys} / {girls} · {gender_unknown} unk.")
    } else {
        format!("{boys} / {girls}")
    };

    let outside_note = if outside_regs.is_empty() {
        String::new()
    } else {
        format!(
            r#"<p class="flash warn">{n} enrollment{s} outside the clinic dates are listed below and excluded from day tabs and summary counts.</p>"#,
            n = outside_regs.len(),
            s = if outside_regs.len() == 1 { "" } else { "s" },
        )
    };
    let mut outside_section = String::new();
    if !outside_regs.is_empty() {
        let mut rows = String::new();
        for r in &outside_regs {
            let patient = patients.get(&r.patient).cloned().unwrap_or_else(|| Patient {
                id: Some(r.patient),
                first: "(missing)".into(),
                ..Patient::default()
            });
            let name = format!(
                "{} {} {}",
                patient.first, patient.paternal_last, patient.maternal_last
            );
            let when = r
                .timein
                .as_deref()
                .and_then(parse_timein)
                .map(|dt| dt.format("%m/%d/%Y %H:%M").to_string())
                .unwrap_or_else(|| "—".into());
            rows.push_str(&format!(
                r#"<tr>
              <td class="photo-cell">{avatar}</td>
              <td>{pid}</td>
              <td>{name}</td>
              <td>{when}</td>
              <td>{dob}</td>
              <td>{gender}</td>
              <td>{curp}</td>
              <td class="actions">
                <a class="btn" href="/patients/{pid}/edit">Edit</a>
                <form class="inline" method="post" action="/clinics/{cid}/unregister/{rid}" onsubmit="return confirm('Unregister this patient?');">
                  <button type="submit" class="btn danger">Unregister</button>
                </form>
              </td>
            </tr>"#,
                avatar = headshot_img(r.patient, "sm", name.trim()),
                pid = r.patient,
                name = escape(name.trim()),
                when = escape(&when),
                dob = escape(&patient.dob),
                gender = escape(&patient.gender),
                curp = curp_cell(&patient.curp),
                cid = id,
                rid = r.id,
            ));
        }
        outside_section = format!(
            r#"<h2>Outside clinic dates</h2>
    <p class="muted">Enrollments with check-in times before {start} or after {end} (often made between clinics). Not used for performance stats.</p>
    <table>
      <thead><tr><th></th><th>Patient ID</th><th>Name</th><th>Check-in</th><th>DOB</th><th>Gender</th><th>CURP</th><th></th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"#,
            start = escape(&format_mdy(clinic.start)),
            end = escape(&format_mdy(clinic.end)),
            rows = rows,
        );
    }

    let body = format!(
        r#"
    <h1>Clinic {id}</h1>
    {flash}
    {outside_note}
    <dl class="clinic-meta">
      <div><dt>Location</dt><dd>{loc}</dd></div>
      <div><dt>Dates</dt><dd>{dates}</dd></div>
      <div><dt>Unique patients</dt><dd>{unique}</dd></div>
      <div><dt>Boys / girls</dt><dd>{boys_girls}</dd></div>
      <div><dt>Check-ins</dt><dd>{checkins}</dd></div>
    </dl>
    <div class="toolbar">
      {register_link}
      <a class="btn" href="/clinics/{id}/stats">Stats</a>
      <a class="btn" href="/patients/new">New patient</a>
      <a class="btn" href="/patients/search">Find patient</a>
      <a class="btn" href="/clinics">Back to clinics</a>
    </div>
    {day_section}
    {outside_section}
    "#,
        id = id,
        loc = escape(&loc),
        flash = flash,
        outside_note = outside_note,
        dates = escape(&dates),
        unique = unique_patients,
        boys_girls = escape(&boys_girls),
        checkins = regs.len(),
        register_link = register_link,
        day_section = day_section,
        outside_section = outside_section,
    );

    Ok(layout("Clinic", &body).into_response())
}

/// Compact CURP: first 8 chars, full value on hover, copy + official lookup.
fn curp_cell(curp: &str) -> String {
    let curp = curp.trim();
    if curp.is_empty() {
        return r#"<span class="muted">—</span>"#.into();
    }
    let short: String = {
        let mut chars = curp.chars();
        let head: String = chars.by_ref().take(8).collect();
        if chars.next().is_some() {
            format!("{head}…")
        } else {
            head
        }
    };
    let full = escape(curp);
    // Public gob.mx CURP page (direct consultas.curp.gob.mx deep-links are often blocked).
    // CURP is copied so it can be pasted into the official search form.
    let lookup = "https://www.gob.mx/curp/";
    format!(
        r#"<span class="curp-cell" title="{full}">
      <code class="curp-short">{short}</code>
      <button type="button" class="icon-btn" data-copy="{full}" title="Copy full CURP" aria-label="Copy CURP">
        <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
        </svg>
      </button>
      <a class="icon-btn curp-lookup" href="{lookup}" target="_blank" rel="noopener noreferrer"
         data-copy="{full}"
         title="Open gob.mx CURP lookup (new tab). CURP is copied — paste into the form to search."
         aria-label="Look up CURP on gob.mx">
        <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path fill="currentColor" d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
        </svg>
      </a>
    </span>"#,
        full = full,
        short = escape(&short),
        lookup = lookup,
    )
}

fn error_page(msg: &str) -> Response {
    layout("Error", &flash_err(msg)).into_response()
}
