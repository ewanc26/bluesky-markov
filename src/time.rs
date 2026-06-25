//! Timing utilities for the bot's refresh-sleep cycle.
//!
//! The bot doesn't post on a fixed schedule — it picks a random interval
//! between 30 minutes and 3 hours so the output feels organic rather than
//! clockwork.

use chrono::{DateTime, Local, Duration};
use rand::Rng;
use tracing::{debug, info, warn};
use tokio::time::sleep;

/// Pick a random refresh interval between 30 min and 3 hours.
///
/// Jitter avoids predictable posting patterns that might look like spam.
pub fn calculate_refresh_interval() -> i64 {
    let mut rng = rand::thread_rng();
    let refresh_interval = rng.gen_range(1800..10800);
    debug!("Calculated refresh interval: {} seconds", refresh_interval);
    refresh_interval
}

/// Compute the next absolute wall-clock time to wake up.
pub fn calculate_next_refresh(current_time: DateTime<Local>, refresh_interval: i64) -> DateTime<Local> {
    let next_refresh = current_time + Duration::seconds(refresh_interval);
    debug!("Calculated next refresh time: {}", next_refresh);
    next_refresh
}

/// Format a Duration into a human-readable "X hours, Y minutes, Z seconds" string.
pub fn format_time_remaining(time_remaining: Duration) -> String {
    let total_seconds = time_remaining.num_seconds();
    let hours = total_seconds / 3600;
    let minutes = (total_seconds % 3600) / 60;
    let seconds = total_seconds % 60;
    format!(
        "{} hour{}, {} minute{}, {} second{}",
        hours,
        if hours != 1 { "s" } else { "" },
        minutes,
        if minutes != 1 { "s" } else { "" },
        seconds,
        if seconds != 1 { "s" } else { "" }
    )
}

/// Block (async) until the next refresh time arrives.
///
/// Logs a warning if the target is already in the past — this shouldn't
/// happen in normal operation unless the clock was adjusted.
pub async fn sleep_until_next_refresh(next_refresh: DateTime<Local>) {
    let current_time = Local::now();
    let time_remaining = next_refresh - current_time;

    if time_remaining.num_seconds() > 0 {
        println!("Time until next post refresh: {}", format_time_remaining(time_remaining));
        info!("Sleeping for {} seconds until next refresh.", time_remaining.num_seconds());
        sleep(tokio::time::Duration::from_secs(time_remaining.num_seconds() as u64)).await;
    } else {
        warn!("Next refresh time is in the past. No sleep required.");
    }
}
