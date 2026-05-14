#!/usr/bin/env bash
set -euo pipefail

echo "=== Day 19 Secret Safety Check ==="

echo "Checking for tracked env files..."
git ls-files | grep -E '(^|/)\.env($|\.)|(^|/)docker\.env$|(^|/)\.env\.compose$' && { 
    echo "❌ Tracked secret-like env file found. Fix this."
    exit 1
} || echo "✓ No env files tracked in git"

echo "Checking for obvious hardcoded secret markers..."
grep -RIn --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.cache \
    --exclude=settings.py \
    -E 'GROQ_API_KEY\s*=\s*"[^"]+"|API_KEY\s*=\s*"[^"]+"' src/ || true

echo "✓ Secret-safety check completed."
