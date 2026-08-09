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

use axum::http::StatusCode;
use axum::response::{IntoResponse, Redirect, Response};
use tower_sessions::Session;

pub const SESSION_TOKEN: &str = "tscharts_token";
pub const SESSION_USER: &str = "tscharts_user";

pub async fn require_token(session: &Session) -> Result<String, Response> {
    match session.get::<String>(SESSION_TOKEN).await {
        Ok(Some(token)) if !token.is_empty() => Ok(token),
        Ok(_) => Err(Redirect::to("/login").into_response()),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR.into_response()),
    }
}

pub async fn set_auth(session: &Session, token: &str, username: &str) -> Result<(), Response> {
    session
        .insert(SESSION_TOKEN, token.to_string())
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR.into_response())?;
    session
        .insert(SESSION_USER, username.to_string())
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR.into_response())?;
    Ok(())
}

pub async fn clear_auth(session: &Session) {
    let _ = session.flush().await;
}
