# Automation

Python (Netmiko) and Bash tooling that runs against the lab devices.

> 🟡 **In progress.** Built and tested live against the Lab 01 VyOS routers.

## Scripts (planned / in progress)

| Script | What it does |
|--------|--------------|
| `config_backup.py` | Netmiko multi-device config backup. Reads an inventory from YAML, connects to each device, saves a timestamped config. Credentials come from `getpass`/environment variables — **never hardcoded**. |
| `compliance_audit.py` | Checks each device against a baseline — interface descriptions present, unused ports shut, NTP/SSH/banner set — and prints pass/fail. |
| `backup.sh` | Bash wrapper / cron-able runner for `config_backup.py`. |
| `inventory.example.yml` | Sanitized example inventory. The real `inventory.yml` is git-ignored. |

## Principles
- **No hardcoded credentials.** Secrets come from environment variables or an interactive prompt.
- **Parameterized inventory.** Devices live in YAML, not in the code — add a device by editing data, not logic.
- The real inventory and any backups are excluded via `.gitignore`.

## Setup (planned)
```bash
python3 -m venv venv
source venv/bin/activate
pip install netmiko
cp inventory.example.yml inventory.yml   # then edit with real (git-ignored) values
```
