# Network Lab Portfolio

Hands-on networking labs and automation I built, configured, and verified myself — documented with real device output, design rationale, and lessons learned. Built to demonstrate practical routing, switching, security, and automation skills beyond certification.

**Alexander Hassel** — IT professional moving into network engineering (Tucson, AZ)

### Certifications
- Cisco **CCNA**
- CompTIA **Security+**
- CompTIA **Network+**
- Fortinet **FCP – Network Security** *(in progress)*

### Tools used
GNS3 · VyOS · FRRouting · Cisco Packet Tracer · Linux · Python (Netmiko) · Git

---

## Labs

| # | Lab | Focus | Status |
|---|-----|-------|--------|
| 01 | [Multi-site OSPF + IPsec VPN](labs/01-multisite-ospf-vpn/) | Multi-area OSPF (backbone + stub areas), site-to-site IPsec, hub-and-spoke WAN | 🟢 OSPF complete · IPsec in progress |
| 02 | [FortiGate Firewall Policy](labs/02-fortigate-firewall-policy/) | LAN/DMZ/WAN zones, NAT, deny-by-default policy, logging | 🟡 Built & documented · transit blocked by invalid eval license (troubleshooting artifact) |
| 03 | [Campus VLAN / STP](labs/03-campus-vlan-stp/) | Collapsed core, 802.1Q trunks, Rapid-PVST+, port security, inter-VLAN routing | 🟢 Complete |

## Automation
[`automation/`](automation/) — Python (Netmiko) and Bash tooling that runs against the lab devices: multi-device config backup and a compliance audit against a baseline. Credentials are never hardcoded.

---

📫 **LinkedIn:** [linkedin.com/in/alexanderdhassel08](https://linkedin.com/in/alexanderdhassel08)
