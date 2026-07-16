# AGENTS.md

Guidance for agents working on the Rust Bluesky Markov bot.

## Data flow

The bot authenticates source and destination accounts, fetches source posts, cleans text, trains a Markov chain, generates bounded content, publishes to the destination account, and schedules later runs. Configuration comes from `.env`; logs are rotated locally.

## Invariants

- Keep source reads and destination writes distinct. Never post using the source session or fetch private data unnecessarily.
- Exclude repost wrappers, unsuitable/empty text, and malformed records consistently; HTML/entity cleanup must not corrupt Unicode.
- Generated posts must obey the configured character limit and must not busy-loop when generation repeatedly fails.
- Validate scheduling bounds, use bounded backoff, and respect rate limits.
- Never log app passwords, access/refresh tokens, or authorization headers.
- Preserve unknown profile/record fields when interacting with AT Protocol records.

## Validation

Run `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test`, and `cargo build --release`. Mock AT Protocol clients and time for source pagination, empty corpus, Unicode, over-limit generation, authentication failure, write failure, retry bounds, and shutdown. A live post is not a routine test; use a dedicated test account only when explicitly appropriate. Do not commit `.env` or logs.
