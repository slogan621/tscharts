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

//! Session-authenticated headshot proxy + upload/replace.

use axum::body::Body;
use axum::extract::{Multipart, Path, Query, State};
use axum::http::{header, HeaderValue, StatusCode};
use axum::response::{IntoResponse, Redirect, Response};
use base64::Engine;
use serde::Deserialize;
use tower_sessions::Session;

use crate::html::{flash_err, layout};
use crate::session::require_token;
use crate::AppState;

fn decode_image_b64(raw: &str) -> anyhow::Result<Vec<u8>> {
    let s = raw.trim();
    let s = if let Some(idx) = s.find("base64,") {
        &s[idx + "base64,".len()..]
    } else {
        s
    };
    let s: String = s.chars().filter(|c| !c.is_whitespace()).collect();
    base64::engine::general_purpose::STANDARD
        .decode(s.as_bytes())
        .or_else(|_| base64::engine::general_purpose::STANDARD_NO_PAD.decode(s.as_bytes()))
        .map_err(|e| anyhow::anyhow!("base64 decode: {e}"))
}

fn content_type_for(bytes: &[u8]) -> &'static str {
    if bytes.len() >= 3 && bytes[0] == 0xFF && bytes[1] == 0xD8 && bytes[2] == 0xFF {
        "image/jpeg"
    } else if bytes.len() >= 8 && bytes.starts_with(&[0x89, b'P', b'N', b'G']) {
        "image/png"
    } else if bytes.len() >= 6 && (bytes.starts_with(b"GIF87a") || bytes.starts_with(b"GIF89a")) {
        "image/gif"
    } else if bytes.len() >= 12 && bytes.starts_with(b"RIFF") {
        "image/webp"
    } else {
        "application/octet-stream"
    }
}

fn placeholder_svg() -> Response {
    let svg = r##"<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <rect width="128" height="128" fill="#e7eee9"/>
  <circle cx="64" cy="48" r="22" fill="#b7c4bb"/>
  <ellipse cx="64" cy="106" rx="36" ry="28" fill="#b7c4bb"/>
</svg>"##;
    (
        StatusCode::OK,
        [
            (
                header::CONTENT_TYPE,
                HeaderValue::from_static("image/svg+xml"),
            ),
            (
                header::CACHE_CONTROL,
                HeaderValue::from_static("private, max-age=60"),
            ),
        ],
        Body::from(svg),
    )
        .into_response()
}

/// GET /patients/:id/headshot — proxy newest Headshot for <img src>.
pub async fn get_headshot(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
) -> Response {
    let token = match require_token(&session).await {
        Ok(t) => t,
        Err(resp) => return resp,
    };
    match state.api.get_newest_headshot(&token, id).await {
        Ok(Some(img)) => match decode_image_b64(&img.data) {
            Ok(bytes) if !bytes.is_empty() => {
                let ct = content_type_for(&bytes);
                (
                    StatusCode::OK,
                    [
                        (
                            header::CONTENT_TYPE,
                            HeaderValue::from_static(ct),
                        ),
                        (
                            header::CACHE_CONTROL,
                            HeaderValue::from_static("private, max-age=120"),
                        ),
                    ],
                    Body::from(bytes),
                )
                    .into_response()
            }
            _ => placeholder_svg(),
        },
        _ => placeholder_svg(),
    }
}

#[derive(Deserialize)]
pub struct HeadshotUploadQuery {
    #[serde(default)]
    clinic: Option<i64>,
}

/// POST /patients/:id/headshot — multipart field `photo`; replaces prior headshots.
pub async fn upload_headshot(
    State(state): State<AppState>,
    session: Session,
    Path(id): Path<i64>,
    Query(q): Query<HeadshotUploadQuery>,
    mut multipart: Multipart,
) -> Result<Response, Response> {
    let token = require_token(&session).await?;

    let mut file_bytes: Option<Vec<u8>> = None;
    while let Some(field) = multipart
        .next_field()
        .await
        .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?
    {
        if field.name() == Some("photo") {
            let data = field
                .bytes()
                .await
                .map_err(|e| layout("Error", &flash_err(&e.to_string())).into_response())?;
            file_bytes = Some(data.to_vec());
        }
    }

    let bytes = match file_bytes {
        Some(b) if !b.is_empty() => b,
        _ => {
            return Ok(Redirect::to(&format!(
                "/patients/{id}/edit?err=Choose%20a%20photo%20file%20to%20upload"
            ))
            .into_response());
        }
    };

    if bytes.len() > 12 * 1024 * 1024 {
        return Ok(Redirect::to(&format!(
            "/patients/{id}/edit?err=Photo%20too%20large%20(max%2012MB)"
        ))
        .into_response());
    }

    let b64 = base64::engine::general_purpose::STANDARD.encode(&bytes);

    // Collect existing headshots so we can remove them after a successful upload.
    let old_ids = state
        .api
        .list_headshot_ids(&token, id)
        .await
        .unwrap_or_default();

    match state
        .api
        .create_headshot(&token, id, &b64, q.clinic)
        .await
    {
        Ok(_new_id) => {
            for old in old_ids {
                let _ = state.api.delete_image(&token, old).await;
            }
            Ok(Redirect::to(&format!("/patients/{id}/edit?msg=Headshot%20updated")).into_response())
        }
        Err(e) => Ok(Redirect::to(&format!(
            "/patients/{id}/edit?err={}",
            urlencoding::encode(&e.to_string())
        ))
        .into_response()),
    }
}
