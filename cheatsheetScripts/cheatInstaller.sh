#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p ~/.local/bin
cp "$DIR/cheat.py" ~/.local/bin/cheat
chmod +x ~/.local/bin/cheat

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  source ~/.bashrc
fi

echo "✓ Done! Run: cheat"