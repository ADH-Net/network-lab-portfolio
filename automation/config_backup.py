#!/usr/bin/env python3
"""
config_backup.py — Back up network device configs over SSH using Netmiko.

Reads a device inventory from YAML, connects to each device, pulls its
configuration, and writes a timestamped file to ./backups/.

Credentials are NEVER hardcoded — they come from the environment
(NET_USER / NET_PASS) or an interactive prompt.

Usage:
    python config_backup.py [inventory.yml]
"""

import os
import sys
import getpass
import datetime
from pathlib import Path

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# The command that dumps the config, chosen per Netmiko device_type.
BACKUP_COMMAND = {
    "vyos": "show configuration commands",
    "cisco_ios": "show running-config",
}
BACKUP_DIR = Path("backups")


def load_inventory(path):
    """Read the YAML inventory; return (defaults, devices)."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("defaults", {}), data.get("devices", [])


def get_credentials():
    """Credentials from env vars, falling back to an interactive prompt.
    Never store these in the script or the inventory."""
    username = os.environ.get("NET_USER") or input("Username: ")
    password = os.environ.get("NET_PASS") or getpass.getpass("Password: ")
    return username, password


def backup_device(device, defaults, username, password):
    """Connect to one device, fetch its config, save it; return the file path."""
    device_type = device.get("device_type", defaults.get("device_type"))
    name = device["name"]

    connection = {
        "device_type": device_type,
        "host": device["host"],
        "username": username,
        "password": password,
    }
    command = BACKUP_COMMAND.get(device_type, "show running-config")

    # 'with' guarantees the SSH session closes even if something errors.
    with ConnectHandler(**connection) as conn:
        config = conn.send_command(command, read_timeout=60)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUP_DIR.mkdir(exist_ok=True)
    out_path = BACKUP_DIR / f"{name}_{timestamp}.conf"
    out_path.write_text(config + "\n")
    return out_path


def main():
    inventory_path = sys.argv[1] if len(sys.argv) > 1 else "inventory.yml"
    defaults, devices = load_inventory(inventory_path)
    if not devices:
        sys.exit(f"No devices found in {inventory_path}")

    username, password = get_credentials()

    print(f"\nBacking up {len(devices)} device(s)...\n")
    ok = failed = 0
    for device in devices:
        name = device["name"]
        try:
            path = backup_device(device, defaults, username, password)
            print(f"  [ OK ]   {name:10} -> {path}  ({path.stat().st_size} bytes)")
            ok += 1
        except NetmikoAuthenticationException:
            print(f"  [FAIL]   {name:10} -> authentication failed (check credentials)")
            failed += 1
        except NetmikoTimeoutException:
            print(f"  [FAIL]   {name:10} -> timed out (unreachable / SSH down)")
            failed += 1
        except Exception as e:
            print(f"  [FAIL]   {name:10} -> {type(e).__name__}: {e}")
            failed += 1

    print(f"\nDone. {ok} succeeded, {failed} failed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
