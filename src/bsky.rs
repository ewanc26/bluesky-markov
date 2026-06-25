//! Bluesky session management — login and DID resolution.
//!
//! Wraps bsky-sdk authentication so the caller only needs env-var names.
//! The agent returned by `login` is used for all subsequent API calls.

use bsky_sdk::BskyAgent;
use bsky_sdk::agent::config::Config;
use atrium_api::types::string::Did;
use anyhow::{Result, Context, anyhow};
use std::env;
use tracing::{info, debug};

/// Authenticate against the Bluesky PDS (public or self-hosted).
///
/// Reads the handle and app-password from environment variables named by
/// `handle_env_var` and `app_pass_env_var`. The PDS endpoint defaults to
/// `https://bsky.social` but can be overridden with `BSKY_HOST_URL`.
///
/// Returns an authenticated `BskyAgent` ready for API calls.
pub async fn login(handle_env_var: &str, app_pass_env_var: &str) -> Result<BskyAgent> {
    let handle = env::var(handle_env_var).with_context(|| format!("Missing env var {}", handle_env_var))?;
    let app_pass = env::var(app_pass_env_var).with_context(|| format!("Missing env var {}", app_pass_env_var))?;
    let host_url = env::var("BSKY_HOST_URL").unwrap_or_else(|_| "https://bsky.social".to_string());

    debug!("Attempting to log in with handle: {}", handle);

    let agent = BskyAgent::builder()
        .config(Config {
            endpoint: host_url,
            ..Default::default()
        })
        .build()
        .await?;

    agent.login(handle.clone(), app_pass).await?;

    info!("Login successful for handle: {}", handle);
    Ok(agent)
}

/// Resolve a handle (e.g. `@user.bsky.social`) to its DID.
///
/// Required before fetching records — the AT Protocol identifies repos by
/// DID, not handle.
pub async fn resolve_did(agent: &BskyAgent, handle: &str) -> Result<Did> {
    debug!("Resolving DID for handle: {}", handle);
    let output = agent.api.com.atproto.identity.resolve_handle(
        atrium_api::com::atproto::identity::resolve_handle::ParametersData {
            handle: handle.parse().map_err(|e| anyhow!("{:?}", e))?,
        }.into()
    ).await?;

    let did = output.data.did;
    debug!("Resolved DID: {}", did.as_str());
    Ok(did)
}
