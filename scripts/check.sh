#!/usr/bin/env bash
# The one check agents and CI run before calling a change done.
set -euo pipefail
cd "$(dirname "$0")/.."

# MSYS_NO_PATHCONV keeps Git Bash from rewriting the container paths; pwd -W gives Docker a Windows path.
export MSYS_NO_PATHCONV=1
repo="$(pwd -W 2>/dev/null || pwd)"

docker run --rm -v "$repo:/repo:ro" -w /repo ghcr.io/astral-sh/ruff:0.8.2 check --no-cache .
docker run --rm -v "$repo:/repo:ro" -w /repo -e PYTHONPYCACHEPREFIX=/tmp/pyc python:3.11-slim python -m compileall -q src
