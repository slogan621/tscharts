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
    document.addEventListener("click", async (event) => {{
      const btn = event.target.closest("[data-copy]");
      if (!btn) return;
      const text = btn.getAttribute("data-copy") || "";
      try {{
        await navigator.clipboard.writeText(text);
        btn.classList.add("copied");
        window.setTimeout(() => btn.classList.remove("copied"), 1200);
      }} catch (_err) {{
        window.prompt("Copy CURP:", text);
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
