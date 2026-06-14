use regex::Regex;
use html_escape::decode_html_entities;
use tracing::debug;

pub fn clean_content(content: &str) -> String {
    debug!("Original content: {}", content);

    // Remove HTML tags
    let re_html = Regex::new(r"<[^<]+?>").unwrap();
    let cleaned = re_html.replace_all(content, "");
    debug!("After removing HTML tags: {}", cleaned);

    // Decode HTML entities
    let cleaned = decode_html_entities(&cleaned);
    debug!("After decoding HTML entities: {}", cleaned);

    // Remove usernames based on domain patterns
    let domain_regex = Regex::new(r"@\w+\.([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?").unwrap();
    let cleaned = domain_regex.replace_all(&cleaned, "");
    debug!("After removing usernames: {}", cleaned);

    // Remove special characters (preserving some punctuation)
    let re_special = Regex::new(r"[^\w\s.,!?;:]").unwrap();
    let cleaned = re_special.replace_all(&cleaned, "");
    debug!("After removing special characters: {}", cleaned);

    // Remove words enclosed with colons (emojis etc)
    let re_colons = Regex::new(r":\w+:").unwrap();
    let cleaned = re_colons.replace_all(&cleaned, "");
    debug!("After removing words enclosed with colons: {}", cleaned);

    cleaned.to_string().trim().to_string()
}
