# Lab 02 — FortiGate Firewall Policy

> ⚪ **Planned.** Built and documented after Lab 01.

A FortiGate firewall between **LAN**, **DMZ**, and **WAN** zones, demonstrating
zone-based policy, NAT, and a deny-by-default posture. Reinforces Fortinet
FCP – Network Security training.

## Planned scope
- FortiGate VM in GNS3 between LAN / DMZ / WAN zones
- NAT (source NAT for LAN egress; a published DMZ server via VIP/DNAT)
- Policy set: allow web from LAN, publish a DMZ server, **deny-by-default**
- Logging enabled

## Will demonstrate / explain
- Zones and stateful inspection
- Why deny-by-default
- NAT types (SNAT vs DNAT/VIP)
- Policy hit counters; blocked vs. allowed test traffic
