//! Thousand Smiles clinic-ops web dashboard.
//!
//! Axum BFF in front of the tscharts REST API. Imaging is a separate route module.

mod avatar;
mod clinic_filter;
mod clinic_stats;
mod client;
mod config;
mod html;
mod routes;
mod session;

use std::sync::Arc;

use anyhow::Context;
use axum::Router;
use tokio::net::TcpListener;
use tower_http::services::ServeDir;
use tower_http::trace::TraceLayer;
use tower_sessions::{MemoryStore, SessionManagerLayer};
use tracing_subscriber::EnvFilter;

use crate::client::TschartsClient;
use crate::config::Config;

#[derive(Clone)]
pub struct AppState {
    pub api: Arc<TschartsClient>,
    pub config: Arc<Config>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env().add_directive("info".parse()?))
        .init();

    let config = Arc::new(Config::from_env()?);
    let api = Arc::new(TschartsClient::new(&config)?);
    let state = AppState {
        api,
        config: config.clone(),
    };

    let session_store = MemoryStore::default();
    let session_layer = SessionManagerLayer::new(session_store).with_secure(false);

    let static_dir = resolve_static_dir();
    tracing::info!(?static_dir, "serving static assets");

    let app = Router::new()
        .merge(routes::router())
        .nest_service("/static", ServeDir::new(static_dir))
        .layer(session_layer)
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let addr = config.bind_addr()?;
    tracing::info!(
        %addr,
        tscharts = %config.tscharts_base_url,
        "tsdashboard-web listening"
    );
    let listener = TcpListener::bind(addr)
        .await
        .with_context(|| format!("bind {addr}"))?;
    axum::serve(listener, app).await?;
    Ok(())
}

fn resolve_static_dir() -> std::path::PathBuf {
    if let Ok(dir) = std::env::var("STATIC_DIR") {
        return std::path::PathBuf::from(dir);
    }
    let candidates = [
        std::path::PathBuf::from("static"),
        std::path::PathBuf::from("/app/static"),
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("static"),
    ];
    for path in candidates {
        if path.is_dir() {
            return path;
        }
    }
    std::path::PathBuf::from("static")
}
