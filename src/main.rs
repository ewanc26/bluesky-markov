//! Entry point for the bluesky-markov bot.
//!
//! Orchestrates the main loop: fetch source posts, rebuild a Markov chain,
//! generate a new post, publish it to the destination account, then sleep
//! until the next refresh interval.

mod bsky;
mod clean;
mod markov_gen;
mod time;

use anyhow::{Result, Context};
use chrono::Local;
use dotenvy::dotenv;
use std::env;
use std::path::Path;
use tracing::{debug, info, error};
use tracing_subscriber::{fmt, prelude::*, EnvFilter};
use atrium_api::app::bsky::feed::post::RecordData;
use atrium_api::types::string::Datetime;

// ─── Logging & Init ──────────────────────────────────────────────────

#[tokio::main]
async fn main() -> Result<()> {
    // Rolling daily logs under `log/` — survives container restarts
    let log_directory = "log";
    if !Path::new(log_directory).exists() {
        std::fs::create_dir_all(log_directory)?;
    }

    let file_appender = tracing_appender::rolling::daily(log_directory, "general.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

    // Fall back to debug-level if RUST_LOG isn't set
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("debug"));

    tracing_subscriber::registry()
        .with(filter)
        .with(fmt::layer().with_writer(std::io::stdout))
        .with(fmt::layer().with_writer(non_blocking).with_ansi(false))
        .init();

    info!("NEW EXECUTION OF APPLICATION");
    println!("Bluesky Markov Bot started.");

    // ─── Env Config ────────────────────────────────────────────────

    dotenv().ok();

    let source_handle = env::var("SOURCE_HANDLE").context("SOURCE_HANDLE not set")?;
    let destination_handle = env::var("DESTINATION_HANDLE").context("DESTINATION_HANDLE not set")?;
    let char_limit = env::var("CHAR_LIMIT")
        .unwrap_or_else(|_| "280".to_string())
        .parse::<usize>()
        .unwrap_or(280);

    debug!(
        "Loaded environment variables: SOURCE_HANDLE={}, DESTINATION_HANDLE={}, CHAR_LIMIT={}",
        source_handle, destination_handle, char_limit
    );

    // ─── Auth ──────────────────────────────────────────────────────
    // Two separate agents: read-only on source, write-only on destination.
    // App passwords keep the blast radius contained if one is leaked.

    let source_agent = bsky::login("SOURCE_HANDLE", "SRC_APP_PASS").await?;
    let source_did = bsky::resolve_did(&source_agent, &source_handle).await?;

    let destination_agent = bsky::login("DESTINATION_HANDLE", "DST_APP_PASS").await?;

    #[allow(unused_assignments)]
    let mut markov_chain_opt: Option<markov::Chain<String>> = None;

    // ─── Main Loop ─────────────────────────────────────────────────
    // Fetch source posts, rebuild the chain, generate and post, then
    // sleep for a random interval (30 min–3 hours) to avoid bot patterns.

    loop {
        let current_time = Local::now();
        let refresh_interval = time::calculate_refresh_interval();
        let next_refresh = time::calculate_next_refresh(current_time, refresh_interval);

        debug!(
            "Current time: {}, Refresh interval: {}s, Next refresh: {}",
            current_time, refresh_interval, next_refresh
        );

        match markov_gen::retrieve_posts(&source_agent, source_did.clone()).await {
            Ok(posts) => {
                let chain = markov_gen::refresh_dataset(posts);
                markov_chain_opt = Some(chain);
                info!("Markov dataset refreshed.");
                println!("Markov dataset refreshed.");

                if let Some(ref markov_chain) = markov_chain_opt {
                    let generated_text = markov_gen::generate_text(markov_chain, char_limit);
                    info!("Generated text for post: {}", generated_text);

                    if !generated_text.is_empty() {
                        let langs = Some(vec!["en".parse().map_err(|e| anyhow::anyhow!("{:?}", e))?]);
                        match destination_agent.create_record(RecordData {
                            text: generated_text,
                            created_at: Datetime::now(),
                            embed: None,
                            entities: None,
                            facets: None,
                            labels: None,
                            langs,
                            reply: None,
                            tags: None,
                        }).await {
                            Ok(response) => {
                                let post_uri = response.data.uri;
                                info!("Posted to destination Bluesky account successfully: {}", post_uri.as_str());
                                println!("Posted to destination Bluesky account successfully: {}", post_uri.as_str());
                            }
                            Err(err) => {
                                error!("Error posting to destination Bluesky account: {:?}", err);
                            }
                        }
                    }
                }
            }
            Err(e) => {
                error!("Error fetching source posts: {:?}", e);
            }
        }

        time::sleep_until_next_refresh(next_refresh).await;
    }
}
