# Automation

Python (Netmiko) and Bash tooling that runs against the lab devices.

> 🟡 **In progress.** Built and tested live against the Lab 01 VyOS routers.

## Scripts (planned / in progress)

| Script | What it does |
|--------|--------------|
| ✅ `config_backup.py` | Netmiko multi-device config backup. Reads an inventory from YAML, connects to each device, saves a timestamped config. Credentials come from `getpass`/environment variables — **never hardcoded**. *Tested live against the Lab 01 routers.* |
| ✅ `compliance_audit.py` | Checks each device against a baseline — hostname set, SSH/NTP/login-banner present, every addressed interface has a description — and prints PASS/FAIL per check. Exits non-zero if anything fails. *Tested live against the Lab 01 routers.* |
| ✅ `backup.sh` | Bash wrapper / cron-able runner for `config_backup.py` (reads creds from the environment / a git-ignored `.env`). |
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

#### Cron-able backups with `backup.sh`
For unattended runs, `backup.sh` sources credentials from a git-ignored `.env`
(`NET_USER` / `NET_PASS`) and runs the backup — drop it in cron for scheduled,
hands-off config backups.

## Running `compliance_audit.py`
```bash
NET_USER=vyos python compliance_audit.py inventory.yml
```

### Sample run — closed-loop compliance (before → after)
The audit caught a missing login banner on every device, then confirmed
compliance after remediation.

**Before** (no login banner configured):
```
=== HQ (host) ===
  [PASS] hostname set       : HQ
  [PASS] SSH enabled        : service ssh present
  [PASS] NTP configured     : ntp server configured
  [FAIL] login banner       : login banner set
  [PASS] iface descriptions : 4 addressed interfaces all described
  ... (Branch1, Branch2 likewise) ...

Audit complete. 3 failed check(s).
```

**After** (`set system login banner pre-login '...'` applied to all three):
```
=== HQ (host) ===
  [PASS] hostname set       : HQ
  [PASS] SSH enabled        : service ssh present
  [PASS] NTP configured     : ntp server configured
  [PASS] login banner       : login banner set
  [PASS] iface descriptions : 4 addressed interfaces all described
  ... (Branch1, Branch2 likewise) ...

Audit complete. 0 failed check(s).
```
