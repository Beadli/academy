#!/usr/bin/env python3
"""Generate the two CyberRack companion diagrams.

Palette, stroke weights and type scale are lifted from Steve's
cyberrack_v1_1_rack_elevation.svg so the three read as one set.
"""
import pathlib

STYLE = """<style>
.bg{fill:#f7f5ef}
.card{fill:#fbfaf6;stroke:#737981;stroke-width:2}
.band{fill:#f3f1eb;stroke:#c9ccc5;stroke-width:1.5}
.node{fill:#dce8df;stroke:#6f8c78;stroke-width:2}
.neutral{fill:#f3f1eb;stroke:#4d535a;stroke-width:2}
.chip{fill:#fbfaf6;stroke:#a8adb3;stroke-width:1.5}
.chipAccent{fill:#dce8df;stroke:#6f8c78;stroke-width:1.5}
.dark{fill:#3a3f45;stroke:#1f2327;stroke-width:2}
.wire{fill:none;stroke:#4d535a;stroke-width:2.5}
.trunk{fill:none;stroke:#2d3136;stroke-width:9;stroke-linecap:round}
.vlanline{fill:none;stroke:#6f8c78;stroke-width:2}
.dashed{fill:none;stroke:#a8adb3;stroke-width:2;stroke-dasharray:8 7}
.title{font:700 42px Arial,sans-serif;fill:#20252a}
.sub{font:19px Arial,sans-serif;fill:#555b63}
.bandlbl{font:700 15px Arial,sans-serif;fill:#496654;letter-spacing:1.5px}
.bandsub{font:14px Arial,sans-serif;fill:#6b7178}
.colhead{font:700 19px Arial,sans-serif;fill:#252a2f}
.colsub{font:14px Arial,sans-serif;fill:#5f666d}
.label{font:700 17px Arial,sans-serif;fill:#252a2f}
.body{font:16px Arial,sans-serif;fill:#343a40}
.small{font:14px Arial,sans-serif;fill:#5f666d}
.mono{font:700 15px "Courier New",monospace;fill:#343a40}
.monosm{font:14px "Courier New",monospace;fill:#5f666d}
.foot{font:14px Arial,sans-serif;fill:#8b9198}
</style>"""


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def txt(x, y, s, cls='body', anchor='start'):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{x}" y="{y}" class="{cls}"{a}>{esc(s)}</text>'


def rect(x, y, w, h, cls, r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>'


# ---------------------------------------------------------------- diagram 1
def stack():
    W, H = 1800, 1024
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="CyberRack service stack: '
         'three matched mini PCs named Atlas, Hermes and Daedalus each running Proxmox VE, '
         'a storage appliance running TrueNAS SCALE, and a mini PC running OPNsense, shown as '
         'three layers: the hardware each sits on, the platform that runs on the hardware, and '
         'the services a user actually logs into.">',
         STYLE, rect(0, 0, W, H, 'bg', 0)]

    o.append(txt(90, 74, 'CyberRack v1.1 · what runs where', 'title'))
    o.append(txt(90, 112, 'the same rack read as three layers: hardware, the platform on it, '
                          'and the services you actually log into', 'sub'))

    cols = [
        ('Atlas', 'identity', True, 'Lenovo ThinkCentre M920q', '64 GB · Proxmox VE',
         ['Active Directory', 'AD Certificate Services', 'Keycloak', 'DNS and DHCP']),
        ('Hermes', 'security', True, 'Lenovo ThinkCentre M920q', '64 GB · Proxmox VE',
         ['Wazuh (SIEM)', 'Suricata (IDS)', 'log collection', 'Grafana dashboards']),
        ('Daedalus', 'platform', True, 'Lenovo ThinkCentre M920q', '64 GB · Proxmox VE',
         ['Docker', 'k3s', 'Gitea', 'CI/CD runners']),
        ('Storage', 'data', False, 'AOOSTAR WTR Pro', '2 × 4 TB · TrueNAS SCALE',
         ['NFS and SMB shares', 'iSCSI targets', 'ZFS snapshots', 'replication targets']),
        ('Firewall', 'edge', False, 'Intel N100 mini PC', 'dual-port · OPNsense',
         ['VLAN routing', 'firewall policy', 'VPN', 'IDS and IPS']),
    ]

    LX, CX0, CW, GAP = 90, 330, 262, 22
    HEAD_Y = 250
    SVC_Y, SVC_H = 280, 300
    PLT_Y, PLT_H = 610, 96
    HW_Y, HW_H = 736, 96

    # band labels down the left
    for y, h, lbl, sub in [
        (SVC_Y, SVC_H, 'SERVICES', 'what you log into'),
        (PLT_Y, PLT_H, 'PLATFORM', 'what runs them'),
        (HW_Y, HW_H, 'HARDWARE', 'what it sits on'),
    ]:
        o.append(rect(LX, y, 1668, h, 'band', 10))
        o.append(txt(LX + 22, y + 34, lbl, 'bandlbl'))
        o.append(txt(LX + 22, y + 58, sub, 'bandsub'))

    for i, (name, role, accent, hw1, hw2, svcs) in enumerate(cols):
        x = CX0 + i * (CW + GAP)
        o.append(txt(x + CW / 2, HEAD_Y - 26, name, 'colhead', 'middle'))
        o.append(txt(x + CW / 2, HEAD_Y - 4, role, 'colsub', 'middle'))

        for j, s in enumerate(svcs):                      # services
            cy = SVC_Y + 24 + j * 64
            o.append(rect(x, cy, CW, 50, 'chipAccent' if accent else 'chip', 8))
            o.append(txt(x + CW / 2, cy + 31, s, 'body', 'middle'))

        o.append(rect(x, PLT_Y + 20, CW, 56, 'node' if accent else 'neutral', 8))
        o.append(txt(x + CW / 2, PLT_Y + 54, hw2.split(' · ')[-1], 'label', 'middle'))

        o.append(rect(x, HW_Y + 20, CW, 56, 'neutral', 8))
        o.append(txt(x + CW / 2, HW_Y + 44, hw1, 'small', 'middle'))
        o.append(txt(x + CW / 2, HW_Y + 64, hw2.split(' · ')[0], 'small', 'middle'))

    # the point of the whole picture
    y = 866
    o.append(rect(90, y, 1668, 96, 'card', 10))
    o.append(txt(114, y + 36, 'The three green nodes are one cluster, not three servers.', 'label'))
    o.append(txt(114, y + 64, 'Those role names are preferences, not homes. Any workload on Atlas, Hermes or '
                              'Daedalus can move to either of the others while it is still running, which is '
                              'the entire reason for buying three matching machines.', 'small'))

    o.append(txt(1758, 1000, 'designed, not yet built', 'foot', 'end'))
    o.append('</svg>')
    return '\n'.join(o)


# ---------------------------------------------------------------- diagram 2
def network():
    W, H = 1800, 1080
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="CyberRack network: the OPNsense firewall has '
         'two physical interfaces, one WAN facing the internet and one LAN trunk carrying seven tagged '
         'VLANs to a Layer 2 MikroTik switch. Only the WAN interface reaches the internet. Every VLAN is '
         'a sub-interface on the LAN side, and all traffic between VLANs is routed by the firewall.">',
         STYLE, rect(0, 0, W, H, 'bg', 0)]

    o.append(txt(90, 74, 'CyberRack v1.1 · how traffic moves', 'title'))
    o.append(txt(90, 112, 'one cable to the switch, seven networks inside it, and one device deciding '
                          'what may reach what', 'sub'))

    # ---- internet
    o.append(rect(250, 176, 320, 66, 'neutral', 33))
    o.append(txt(410, 216, 'the internet', 'label', 'middle'))
    o.append(f'<path d="M410 242 L410 300" class="wire"/>')
    o.append(txt(424, 278, 'the only way out', 'small'))

    # ---- firewall
    FX, FY, FW, FH = 150, 300, 620, 340
    o.append(rect(FX, FY, FW, FH, 'card', 10))
    o.append(txt(FX + 24, FY + 38, 'OPNsense firewall', 'label'))
    o.append(txt(FX + 24, FY + 60, 'Intel N100 mini PC · two physical ports, no more', 'small'))

    o.append(rect(FX + 24, FY + 78, 180, 44, 'dark', 6))
    o.append(f'<text x="{FX + 114}" y="{FY + 106}" class="mono" style="fill:#f3f1eb" '
             f'text-anchor="middle">WAN  port 1</text>')

    o.append(txt(FX + 24, FY + 156, 'seven VLAN sub-interfaces, all on port 2', 'small'))
    vlans = [('10', 'Management'), ('20', 'Servers'), ('30', 'Backup'), ('40', 'Monitoring'),
             ('50', 'Guest'), ('60', 'IoT'), ('70', 'Security Lab')]
    for i, (vid, nm) in enumerate(vlans):
        cx = FX + 24 + (i % 4) * 145
        cy = FY + 170 + (i // 4) * 48
        o.append(rect(cx, cy, 133, 38, 'chipAccent', 6))
        o.append(txt(cx + 66, cy + 25, f'{vid}  {nm}', 'monosm', 'middle'))

    o.append(rect(FX + 24, FY + 274, 180, 44, 'dark', 6))
    o.append(f'<text x="{FX + 114}" y="{FY + 302}" class="mono" style="fill:#f3f1eb" '
             f'text-anchor="middle">LAN  port 2</text>')

    # ---- trunk
    o.append(f'<path d="M{FX + 114} {FY + FH} L{FX + 114} 760" class="trunk"/>')
    o.append(rect(300, 668, 400, 54, 'card', 8))
    o.append(txt(320, 702, 'one cable · seven tagged VLANs · 802.1Q trunk', 'small'))

    # ---- switch
    SX, SY, SW, SH = 150, 760, 620, 108
    o.append(rect(SX, SY, SW, SH, 'neutral', 10))
    o.append(txt(SX + 24, SY + 40, 'MikroTik CRS310 · Layer 2 switch', 'label'))
    o.append(txt(SX + 24, SY + 68, 'passes VLAN tags. Does not route between them.', 'small'))

    # ---- devices
    devs = ['Atlas', 'Hermes', 'Daedalus', 'Storage']
    for i, d in enumerate(devs):
        x = SX + 14 + i * 152
        o.append(f'<path d="M{x + 65} {SY + SH} L{x + 65} 940" class="wire"/>')
        o.append(rect(x, 940, 130, 46, 'chip', 6))
        o.append(txt(x + 65, 969, d, 'small', 'middle'))
    o.append(txt(SX + 24, 1022, 'every device attaches to the switch and to nothing else', 'small'))

    # ---- right column: the two rules that matter
    RX, RW = 880, 830
    o.append(rect(RX, 176, RW, 200, 'card', 10))
    o.append(txt(RX + 26, 216, 'Only one line touches the internet', 'label'))
    o.append(txt(RX + 26, 248, 'Port 1 is the WAN. Everything else in this picture lives behind it.', 'body'))
    o.append(txt(RX + 26, 282, 'The seven VLANs are not seven connections to the outside world. They are', 'body'))
    o.append(txt(RX + 26, 310, 'seven separate networks sharing one cable, kept apart by a tag on every', 'body'))
    o.append(txt(RX + 26, 338, 'frame, and the firewall is the only thing that can carry traffic between them.', 'body'))

    o.append(rect(RX, 406, RW, 232, 'card', 10))
    o.append(txt(RX + 26, 446, 'Why route at the firewall and not the switch', 'label'))
    o.append(txt(RX + 26, 478, 'It costs throughput. Traffic between two VLANs travels up to the firewall', 'body'))
    o.append(txt(RX + 26, 506, 'and back down, capped at what a small N100 box can route. A Layer 3', 'body'))
    o.append(txt(RX + 26, 534, 'switch would move it at line rate and never involve the firewall.', 'body'))
    o.append(txt(RX + 26, 574, 'That is the point. Every crossing passes something that can inspect it:', 'label'))
    o.append(txt(RX + 26, 604, 'Suricata sees it, policy applies to it, and the logs record it. In a lab', 'body'))
    o.append(txt(RX + 26, 626, 'built to practise segmentation, invisible traffic is the failure.', 'body'))

    o.append(rect(RX, 668, RW, 152, 'card', 10))
    o.append(txt(RX + 26, 708, 'VLAN 70 is the one to get right', 'label'))
    o.append(txt(RX + 26, 740, 'Deliberately vulnerable machines live here. It is the segment that must', 'body'))
    o.append(txt(RX + 26, 768, 'not reach anything you care about, and building that boundary yourself', 'body'))
    o.append(txt(RX + 26, 796, 'teaches more than reading about it ever does.', 'body'))

    o.append(rect(RX, 850, RW, 136, 'band', 10))
    o.append(txt(RX + 26, 890, 'This is an SMB pattern, not a large-enterprise one', 'label'))
    o.append(txt(RX + 26, 922, 'Big networks route east-west on Layer 3 switches and save firewalls for', 'body'))
    o.append(txt(RX + 26, 950, 'trust boundaries. Moving some routing to the switch is the phase 2 upgrade.', 'body'))

    o.append(txt(1758, 1056, 'designed, not yet built', 'foot', 'end'))
    o.append('</svg>')
    return '\n'.join(o)


out = pathlib.Path('/home/steve/git/beadli-lab-academy/static/img')
for name, fn in [('cyberrack-stack.svg', stack), ('cyberrack-network.svg', network)]:
    p = out / name
    p.write_text(fn())
    print(f'  wrote {p}  {p.stat().st_size:,} bytes')
