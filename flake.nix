# bluesky-markov dev environment via Nix flakes.
#
# Provides rustc, cargo, rust-analyzer, and the OpenSSL headers needed for
# reqwest/btsky-sdk at link time. Cross-platform: x86_64/aarch64 on Linux/macOS.
{
  description = "bluesky-markov — Markov chain bot for Bluesky (Rust)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      # ── Dev Shell ────────────────────────────────────────────────
      devShells = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              rustc
              cargo
              rust-analyzer
              pkg-config
              openssl
            ];

            shellHook = ''
              echo "bluesky-markov dev shell ready (Rust)"
            '';
          };
        }
      );

      # ── Formatter ────────────────────────────────────────────────
      formatter = forAllSystems (pkgs: pkgs.nixfmt-rfc-style);
    };
}
