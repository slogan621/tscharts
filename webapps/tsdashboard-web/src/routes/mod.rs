mod clinics;
mod headshot;
mod imaging;
mod login;
mod patients;
mod register;

use axum::routing::{get, post};
use axum::Router;

use crate::AppState;

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/", get(clinics::home))
        .route("/login", get(login::login_form).post(login::login_submit))
        .route("/logout", get(login::logout))
        .route("/clinics", get(clinics::list))
        .route("/clinics/new", get(clinics::new_form).post(clinics::create))
        .route("/clinics/:id", get(clinics::detail))
        .route("/clinics/:id/stats", get(clinics::stats))
        .route(
            "/clinics/:id/edit",
            get(clinics::edit_form).post(clinics::update),
        )
        .route("/clinics/:id/delete", post(clinics::delete))
        .route(
            "/clinics/:id/register",
            get(register::register_form).post(register::register_submit),
        )
        .route(
            "/clinics/:clinic_id/unregister/:register_id",
            post(register::unregister),
        )
        .route("/patients/new", get(patients::new_form).post(patients::create))
        .route("/patients/match-check", get(patients::match_check))
        .route(
            "/patients/:id/headshot",
            get(headshot::get_headshot).post(headshot::upload_headshot),
        )
        .route(
            "/patients/:id/edit",
            get(patients::edit_form).post(patients::update),
        )
        .route(
            "/patients/search",
            get(patients::search_form).post(patients::search),
        )
        .route("/imaging", get(imaging::index))
        .route(
            "/imaging/clinic/:clinic_id/patient/:patient_id",
            get(imaging::patient_images),
        )
}
