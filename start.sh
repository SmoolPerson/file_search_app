#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Syncing dependencies..."
uv sync

echo "Starting app..."
uv run streamlit run app.py
