//! Post-text sanitisation pipeline for Markov ingestion.
//!
//! Strips HTML, removes handles, normalises punctuation, and drops
//! colon-emoji noise so the Markov chain sees clean prose tokens.

use regex::Regex;
use html_escape::decode_html_entities;
use tracing::debug;

/// Run the full cleaning pipeline on a post's raw text.
///
/// Steps performed in order:
/// 1. Strip HTML tags (Bluesky rich-text can include them in embedded content)
/// 2. Decode HTML entities (`&amp;` -> `&`, etc.)
/// 3. Remove `@handle.domain` mentions (keep the text, drop the handle syntax)
/// 4. Strip non-word/sentence characters (preserve `.`, `!`, `?`, `;`, `:`)
/// 5. Remove colon-wrapped emotes (`:joy:`)
///
/// The result is trimmed so the chain doesn't learn leading/trailing whitespace.
pub fn clean_content(content: &str) -> String {
    debug!("Original content: {}", content);

    // Step 1: strip any HTML markup that might be mixed into the text
    let re_html = Regex::new(r"<[^<]+?>").unwrap();
    let cleaned = re_html.replace_all(content, "");
    debug!("After removing HTML tags: {}", cleaned);

    // Step 2: resolve HTML entities to their character equivalents
    let cleaned = decode_html_entities(&cleaned);
    debug!("After decoding HTML entities: {}", cleaned);

    // Step 3: remove usernames that include a domain (e.g. @user.bsky.social)
    // Keeps bare @words that might be part of ordinary prose.
    let domain_regex = Regex::new(r"@\w+\.([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?").unwrap();
    let cleaned = domain_regex.replace_all(&cleaned, "");
    debug!("After removing usernames: {}", cleaned);

    // Step 4: keep only word characters, whitespace, and standard sentence punctuation
    let re_special = Regex::new(r"[^\w\s.,!?;:]").unwrap();
    let cleaned = re_special.replace_all(&cleaned, "");
    debug!("After removing special characters: {}", cleaned);

    // Step 5: drop colon-enclosed tokens (:joy:, :thinking:, etc.)
    let re_colons = Regex::new(r":\w+:").unwrap();
    let cleaned = re_colons.replace_all(&cleaned, "");
    debug!("After removing words enclosed with colons: {}", cleaned);

    cleaned.to_string().trim().to_string()
}
