use axum::extract::State;
use axum::response::{IntoResponse, Redirect, Response};
use axum::Form;
use serde::Deserialize;
use tower_sessions::Session;

use crate::html::{escape, flash_err, Html};
use crate::session::{clear_auth, set_auth};
use crate::AppState;

pub async fn login_form() -> Html {
    Html(format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Login · TS Dashboard</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body class="login">
  <main class="card">
    <h1>Login</h1>
    <form method="post" action="/login">
      <label>Username <input name="username" required autocomplete="username"></label>
      <label>Password <input name="password" type="password" required autocomplete="current-password"></label>
      <button type="submit">Sign in</button>
    </form>
  </main>
</body>
</html>"#
    ))
}

#[derive(Deserialize)]
pub struct LoginForm {
    username: String,
    password: String,
}

pub async fn login_submit(
    State(state): State<AppState>,
    session: Session,
    Form(form): Form<LoginForm>,
) -> Response {
    match state.api.login(&form.username, &form.password).await {
        Ok(login) => {
            if let Err(resp) = set_auth(&session, &login.token, &form.username).await {
                return resp;
            }
            Redirect::to("/clinics").into_response()
        }
        Err(e) => Html(format!(
            r#"<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="/static/style.css"><title>Login</title></head>
<body class="login"><main class="card"><h1>Login</h1>
{}
<form method="post" action="/login">
  <label>Username <input name="username" value="{}" required></label>
  <label>Password <input name="password" type="password" required></label>
  <button type="submit">Sign in</button>
</form></main></body></html>"#,
            flash_err(&e.to_string()),
            escape(&form.username)
        ))
        .into_response(),
    }
}

pub async fn logout(session: Session) -> Redirect {
    clear_auth(&session).await;
    Redirect::to("/login")
}
