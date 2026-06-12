#!/usr/bin/env bash
#
# backup.sh — cron-able wrapper for config_backup.py.
#
# Runs an unattended config backup of every device in the inventory.
# Credentials come from the environment (NET_USER / NET_PASS). For scheduled
# (cron) use, put them in a git-ignored .env at the repo root — NEVER commit it:
#
#     NET_USER=vyos
#     NET_PASS=yourpassword
#
# Example cron entry (daily at 02:00):
#     0 2 * * *  /path/to/network-lab-portfolio/automation/backup.sh >> /var/log/netbackup.log 2>&1
#
set -euo pipefail

# Resolve repo root (this script lives in automation/).
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Load credentials from a git-ignored .env if present.
if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    . ./.env
    set +a
fi

# Use the project venv if it exists, else the system python.
PYTHON="./venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON="python3"

exec "$PYTHON" automation/config_backup.py automation/inventory.yml
