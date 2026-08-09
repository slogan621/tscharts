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

//! Runtime config from environment variables.

use anyhow::{Context, Result};
use std::env;

#[derive(Clone, Debug)]
pub struct Config {
    pub tscharts_base_url: String,
    pub listen_addr: String,
    pub tls_insecure: bool,
    pub print_agent_url: Option<String>,
}

impl Config {
    pub fn from_env() -> Result<Self> {
        let _ = dotenvy::dotenv();
        Ok(Self {
            tscharts_base_url: env::var("TSCHARTS_BASE_URL")
                .unwrap_or_else(|_| "https://127.0.0.1".into())
                .trim_end_matches('/')
                .to_string(),
            listen_addr: env::var("LISTEN_ADDR").unwrap_or_else(|_| "0.0.0.0:3000".into()),
            tls_insecure: env::var("TSCHARTS_TLS_INSECURE")
                .map(|v| v == "1" || v.eq_ignore_ascii_case("true"))
                .unwrap_or(false),
            print_agent_url: env::var("PRINT_AGENT_URL").ok().filter(|s| !s.is_empty()),
        })
    }

    pub fn bind_addr(&self) -> Result<std::net::SocketAddr> {
        self.listen_addr
            .parse()
            .with_context(|| format!("invalid LISTEN_ADDR: {}", self.listen_addr))
    }
}
