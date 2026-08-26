#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
zip -r ../language-selector.ankiaddon . \
    --exclude "__pycache__/*" \
    --exclude ".git/*" \
    --exclude ".gitignore" \
    --exclude "package.sh"
echo "Created ../language-selector.ankiaddon"
