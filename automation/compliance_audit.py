#!/usr/bin/env python3
"""
compliance_audit.py — Audit network devices against a config baseline.

Connects to each device in the inventory, pulls its config, and checks it
against baseline rules (hostname, SSH, NTP, login banner, interface
descriptions). Prints PASS/FAIL per check and exits non-zero if any device
fails any check.

Credentials are NEVER hardcoded — env vars (NET_USER / NET_PASS) or a prompt.

Usage:
    python compliance_audit.py [inventory.yml]
"""

import os
import sys
import re
import getpass

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Command that dumps the config, per Netmiko device_type.
AUDIT_COMMAND = {
    "vyos": "show configuration commands",
    "cisco_ios": "show running-config",
}


# --- Baseline checks -------------------------------------------------------
# Each check takes the config text and returns (passed: bool, detail: str).

def check_hostname(cfg):
    m = re.search(r"set system host-name '([^']+)'", cfg)
    if not m:
        return False, "no host-name set"
    if m.group(1).lower() == "vyos":
        return False, "still default 'vyos'"
    return True, m.group(1)


def check_ssh(cfg):
    return ("set service ssh" in cfg), "service ssh present"


def check_ntp(cfg):
    return ("set service ntp server" in cfg), "ntp server configured"


def check_banner(cfg):
    return ("set system login banner" in cfg), "login banner set"


def check_interface_descriptions(cfg):
    """Every interface that has an address must also have a description."""
    addressed = set(re.findall(r"set interfaces (\w+ \w+) address", cfg))
    described = set(re.findall(r"set interfaces (\w+ \w+) description", cfg))
    missing = sorted(addressed - described)
    if missing:
        return False, "missing description on: " + ", ".join(missing)
    return True, f"{len(addressed)} addressed interfaces all described"


# (label, function) — add a rule by adding one line.
BASELINE = [
    ("hostname set",       check_hostname),
    ("SSH enabled",        check_ssh),
    ("NTP configured",     check_ntp),
    ("login banner",       check_banner),
    ("iface descriptions", check_interface_descriptions),
]


# --- Plumbing --------------------------------------------------------------

def load_inventory(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("defaults", {}), data.get("devices", [])


def get_credentials():
    username = os.environ.get("NET_USER") or input("Username: ")
    password = os.environ.get("NET_PASS") or getpass.getpass("Password: ")
    return username, password


def fetch_config(device, defaults, username, password):
    device_type = device.get("device_type", defaults.get("device_type"))
    conn_args = {
        "device_type": device_type,
        "host": device["host"],
        "username": username,
        "password": password,
    }
    command = AUDIT_COMMAND.get(device_type, "show running-config")
    with ConnectHandler(**conn_args) as conn:
        return conn.send_command(command, read_timeout=60)


def main():
    inventory_path = sys.argv[1] if len(sys.argv) > 1 else "inventory.yml"
    defaults, devices = load_inventory(inventory_path)
    if not devices:
        sys.exit(f"No devices found in {inventory_path}")

    username, password = get_credentials()

    total_failures = 0
    for device in devices:
        name = device["name"]
        print(f"\n=== {name} ({device['host']}) ===")
        try:
            cfg = fetch_config(device, defaults, username, password)
        except NetmikoAuthenticationException:
            print("  [ERR ] authentication failed (check credentials)")
            total_failures += 1
            continue
        except NetmikoTimeoutException:
            print("  [ERR ] timed out (unreachable / SSH down)")
            total_failures += 1
            continue
        except Exception as e:
            print(f"  [ERR ] {type(e).__name__}: {e}")
            total_failures += 1
            continue

        for label, check in BASELINE:
            passed, detail = check(cfg)
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {label:18} : {detail}")
            if not passed:
                total_failures += 1

    print(f"\nAudit complete. {total_failures} failed check(s).")
    sys.exit(1 if total_failures else 0)


if __name__ == "__main__":
    main()
