#!/bin/bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

npx -y skills add $REPO/skills -y --global --skill "*" --agent claude-code universal
