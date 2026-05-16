#!/usr/bin/env bash
set -euo pipefail
args=("$@")

if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
  python -m pytest "${args[@]}"
else
  python3 -m pytest "${args[@]}"
fi
