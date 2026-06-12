# Automation

Python (Netmiko) and Bash tooling that runs against the lab devices.

> 🟡 **In progress.** Built and tested live against the Lab 01 VyOS routers.

## Scripts (planned / in progress)

| Script | What it does |
|--------|--------------|
| ✅ `config_backup.py` | Netmiko multi-device config backup. Reads an inventory from YAML, connects to each device, saves a timestamped config. Credentials come from `getpass`/environment variables — **never hardcoded**. *Tested live against the Lab 01 routers.* |
| `compliance_audit.py` | Checks each device against a baseline — interface descriptions present, unused ports shut, NTP/SSH/banner set — and prints pass/fail. |
| `backup.sh` | Bash wrapper / cron-able runner for `config_backup.py`. |
| `inventory.example.yml` | Sanitized example inventory. The real `inventory.yml` is git-ignored. |

## Principles
- **No hardcoded credentials.** Secrets come from environment variables or an interactive prompt.
- **Parameterized inventory.** Devices live in YAML, not in the code — add a device by editing data, not logic.
- The real inventory and any backups are excluded via `.gitignore`.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install netmiko pyyaml
cp inventory.example.yml inventory.yml   # then edit with real (git-ignored) values
```

## Running `config_backup.py`
```bash
# Username via env (not secret); password is prompted securely with getpass.
NET_USER=vyos python config_backup.py inventory.yml
```

### Sample run (live, against the Lab 01 VyOS routers)
```
Password:

Backing up 3 device(s)...

  [ OK ]   HQ         -> backups/HQ_20260612-153818.conf  (2954 bytes)
  [ OK ]   Branch1    -> backups/Branch1_20260612-153824.conf  (2732 bytes)
  [ OK ]   Branch2    -> backups/Branch2_20260612-153830.conf  (2732 bytes)

Done. 3 succeeded, 0 failed.
```
The backups themselves land in `backups/` (git-ignored — raw configs contain
password hashes). Devices are reached over a dedicated out-of-band management
network (`192.168.99.0/24`), separate from the routed/production subnets.
