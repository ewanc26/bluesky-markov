# AGENTS.md

Guidance for agents working on this unmaintained Rust Bluesky Markov bot.

## Repository map

- `src/main.rs` loads `.env`, configures stdout plus daily file logging, logs into separate source and destination accounts, and owns the infinite fetch/post/sleep loop.
- `src/bsky.rs` builds `BskyAgent` sessions and resolves the source handle to a DID.
- `src/markov_gen.rs` paginates `app.bsky.feed.post` records 100 at a time, rebuilds the chain, and generates output.
- `src/clean.rs` strips markup, entities, domain-style mentions, selected punctuation, and colon emotes.
- `src/time.rs` chooses a random 30-minute-to-3-hour local-time delay.
- `src/example.env.txt` is the configuration template; `flake.nix` provides the Rust/OpenSSL development shell.

## Current behaviour and sharp edges

- Reads and writes deliberately use different authenticated agents. Keep source retrieval and destination posting credentials separate.
- Every successfully decoded post record is fed into the corpus, including replies and empty strings after cleaning. There is no filtering by reply/repost semantics or language.
- `CHAR_LIMIT` defaults to 280 when absent or invalid, but is a byte count. `String::truncate` will panic if a generated Unicode string crosses a non-UTF-8 boundary; fix this before claiming Unicode-safe limits.
- A failed fetch or post is only logged; the process still waits for the next random interval. There is no retry/backoff beyond that loop.
- Logging uses `tracing_appender::rolling::daily("log", "general.log")`; files have date suffixes and no retention cleanup. Paths are relative to the process working directory.
- The chain is rebuilt from the complete remote collection on every iteration. Preserve cursor pagination and do not accidentally post with the source agent.
- Never log app passwords, session tokens, or authorization headers, and never commit `.env` or `log/` output.

## Development and validation

Use Rust 1.85 or newer as documented. Run `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test`, and `cargo build --release`; there are currently no checked-in tests, so `cargo test` is only a build-level check. Add unit tests around cleaning, pagination, empty corpora, UTF-8-safe limits, and time calculations when changing those areas. Mock AT Protocol calls for automation. Running the binary can publish a real post and should only be done with explicit test-account credentials.
