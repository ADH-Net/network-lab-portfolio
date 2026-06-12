# Lab 03 — Enterprise Campus VLAN / STP

> ⚪ **Planned.** Built and documented after Labs 01–02.

A collapsed-core campus switching design: VLANs, 802.1Q trunks, Rapid-PVST+
with deliberate root-bridge placement, port security, and inter-VLAN routing.

## Planned scope
- Collapsed core: 2 distribution switches + 2 access switches
- 4+ VLANs with 802.1Q trunks
- Rapid-PVST+ with deliberate root-bridge placement
- Port security on access ports
- SVIs + inter-VLAN routing

## Will demonstrate / explain
- STP root election and why root placement matters
- What port security buys you
- Failover by killing a link (spanning-tree reconvergence)
