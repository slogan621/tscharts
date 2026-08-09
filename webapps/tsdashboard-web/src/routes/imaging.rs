//! Imaging (X-ray) module — separate from clinic ops.
//! View / upload / delete will be implemented here; clinic pages only deep-link in.

use axum::extract::Path;
use axum::response::{IntoResponse, Response};
use tower_sessions::Session;

use crate::html::layout;
use crate::session::require_token;

pub async fn index(session: Session) -> Result<Response, Response> {
    let _ = require_token(&session).await?;
    let body = r#"
    <h1>Imaging</h1>
    <p>X-ray viewing, upload, and deletion live in this module (separate from clinic registration).</p>
    <p class="muted">Open a clinic, then use the <strong>X-rays</strong> link on a registered patient — or implement browse-by-clinic here next.</p>
    <p>Status: <span class="badge current">stub</span> — API wiring coming next.</p>
    "#;
    Ok(layout("Imaging", body).into_response())
}

pub async fn patient_images(
    session: Session,
    Path((clinic_id, patient_id)): Path<(i64, i64)>,
) -> Result<Response, Response> {
    let _ = require_token(&session).await?;
    let body = format!(
        r#"
    <h1>X-rays</h1>
    <p>Clinic <strong>{clinic_id}</strong> · Patient <strong>{patient_id}</strong></p>
    <p class="muted">Stub: list / upload / delete against <code>/tscharts/v1/image/</code> will go here.</p>
    <p><a class="btn" href="/clinics/{clinic_id}">Back to clinic</a></p>
    "#
    );
    Ok(layout("X-rays", &body).into_response())
}
