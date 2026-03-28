#!/bin/bash
# Builds the cheat binary and copies it to ~/.local/bin so you can run "cheat" from anywhere.
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"
/usr/local/go/bin/go build -o cheat .

mkdir -p ~/.local/bin
cp "$DIR/cheat" ~/.local/bin/cheat
chmod +x ~/.local/bin/cheat

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  echo "Added ~/.local/bin to PATH — run: source ~/.bashrc"
fi

echo "✓ Installed. Run: cheat"
