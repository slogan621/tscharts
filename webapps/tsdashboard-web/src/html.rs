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

//! Minimal HTML helpers (no template engine dependency).

use axum::http::{header, HeaderValue, StatusCode};
use axum::response::{IntoResponse, Response};

pub struct Html(pub String);

impl IntoResponse for Html {
    fn into_response(self) -> Response {
        (
            StatusCode::OK,
            [(
                header::CONTENT_TYPE,
                HeaderValue::from_static("text/html; charset=utf-8"),
            )],
            self.0,
        )
            .into_response()
    }
}

pub fn escape(s: &str) -> String {
    s.chars()
        .map(|c| match c {
            '&' => "&amp;".into(),
            '<' => "&lt;".into(),
            '>' => "&gt;".into(),
            '"' => "&quot;".into(),
            '\'' => "&#39;".into(),
            _ => c.to_string(),
        })
        .collect()
}

pub fn layout(title: &str, body: &str) -> Html {
    Html(format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · TS Dashboard</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <header class="top">
    <a class="brand" href="/">Thousand Smiles · Clinic Ops</a>
    <nav>
      <a href="/clinics">Clinics</a>
      <a href="/patients/new">New patient</a>
      <a href="/imaging">Imaging</a>
      <a href="/logout">Logout</a>
    </nav>
  </header>
  <main>
    {body}
  </main>
  <script>
    async function copyText(text) {{
      if (navigator.clipboard && window.isSecureContext) {{
        await navigator.clipboard.writeText(text);
        return;
      }}
      // Fallback for plain HTTP / older browsers — no dialog.
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:fixed;left:-9999px;top:0";
      document.body.appendChild(ta);
      ta.select();
      ta.setSelectionRange(0, ta.value.length);
      const ok = document.execCommand("copy");
      document.body.removeChild(ta);
      if (!ok) throw new Error("copy failed");
    }}
    document.addEventListener("click", async (event) => {{
      const btn = event.target.closest("[data-copy]");
      if (!btn) return;
      const text = btn.getAttribute("data-copy") || "";
      try {{
        await copyText(text);
        btn.classList.add("copied");
        window.setTimeout(() => btn.classList.remove("copied"), 1200);
      }} catch (_err) {{
        // Keep UI quiet if the browser blocks clipboard access.
      }}
    }});
  </script>
</body>
</html>"#,
        title = escape(title),
        body = body
    ))
}

pub fn flash_ok(msg: &str) -> String {
    format!(r#"<p class="flash ok">{}</p>"#, escape(msg))
}

pub fn flash_err(msg: &str) -> String {
    format!(r#"<p class="flash err">{}</p>"#, escape(msg))
}

/// Clipboard copy control (uses global `[data-copy]` handler in [`layout`]).
pub fn copy_icon_btn(value: &str, label: &str) -> String {
    let value = escape(value);
    let label = escape(label);
    format!(
        r#"<button type="button" class="icon-btn" data-copy="{value}" title="{label}" aria-label="{label}">
        <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
        </svg>
      </button>"#
    )
}

/// Numeric ID with a small copy control beside it.
pub fn id_with_copy(id: i64, label: &str) -> String {
    format!(
        r#"<span class="id-cell"><span class="id-num">{id}</span>{btn}</span>"#,
        id = id,
        btn = copy_icon_btn(&id.to_string(), label),
    )
}
