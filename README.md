# 🛡️ soc-homelab-wazuh-elk

![Lab Architecture](https://img.shields.io/badge/Architecture-Virtual%20Lab-blue?style=for-the-badge)
![SIEM](https://img.shields.io/badge/SIEM-Wazuh%20%7C%20ELK-brightgreen?style=for-the-badge)
![NIDS](https://img.shields.io/badge/NIDS-Suricata-red?style=for-the-badge)
![Threat Simulation](https://img.shields.io/badge/Simulation-Atomic%20Red%20Team-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-VirtualBox%20%7C%20VMware-lightgrey?style=for-the-badge)

> **A self-hosted, virtualized Security Operations Center (SOC) for hands-on Blue Team training — featuring centralized log ingestion, network intrusion detection, and automated adversary emulation.**

---

## 📌 Project Overview

This lab simulates an enterprise-grade SOC environment built entirely on local virtual machines. It covers the full detection pipeline: endpoint telemetry collection → network monitoring → log aggregation → alert triage and correlation.

**Core goals:**
- Practice real-world Blue Team workflows (detection engineering, alert triage, threat hunting)
- Validate custom detection rules against known MITRE ATT&CK techniques
- Automate adversary emulation using Atomic Red Team + Python scripting

---

## 🏗️ Architecture & Topology

```
┌──────────────────────────────────────────────────────────────┐
│                        ATTACKER                              │
│          Kali Linux — Automated Attack Generator             │
└────────────────────┬─────────────────────────────────────────┘
                     │ Simulated Attacks
         ┌───────────┴────────────┐
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│  Windows 10     │    │   Ubuntu Server   │
│  Sysmon +       │    │   Wazuh Agent     │
│  Wazuh Agent    │    └────────┬──────────┘
└────────┬────────┘             │
         │  Windows Event Logs  │  Syslog / Auth Logs
         └──────────┬───────────┘
                    ▼
         ┌──────────────────┐
         │  Suricata NIDS   │ ← Network tap
         │  EVE.json alerts │
         └────────┬─────────┘
                  ▼
         ┌──────────────────┐
         │  Wazuh Manager   │
         └────────┬─────────┘
                  ▼
    ┌─────────────────────────┐
    │   ELK Stack             │
    │   Elasticsearch         │
    │   Logstash              │
    │   Kibana Dashboard      │
    └─────────────────────────┘
```

---

## 🛠️ Technology Stack

| Category | Tools |
|---|---|
| SIEM / Log Management | Wazuh, Elasticsearch, Logstash, Kibana |
| Network IDS | Suricata |
| Endpoint Telemetry | Sysmon (Windows) |
| Adversary Emulation | Atomic Red Team, Custom Python Scripts |
| Infrastructure | VirtualBox / VMware |
| OS Targets | Windows 10, Ubuntu 22.04, Kali Linux |

---

## 🚀 Key Features & Capabilities

### 1. Centralized Log Ingestion
Aggregates Windows Event Logs (via Sysmon), Linux auth/syslog, and Suricata network alerts into a unified ELK dashboard for cross-source correlation.

### 2. Custom Detection Engineering
Wrote custom Wazuh decoders and rules to detect specific attack patterns mapped to MITRE ATT&CK, including:
- Privilege escalation via token impersonation
- Lateral movement via PsExec / WMI
- Persistence via scheduled tasks and registry run keys

### 3. Automated Adversary Emulation
Integrated Atomic Red Team with a custom Python automation script (`auto_attack_gen.py`) to programmatically execute attack scenarios across Windows and Linux endpoints — generating realistic telemetry for rule validation.

### 4. Hands-on Alert Triage
Queried Elasticsearch with KQL, correlated multi-source events, and tuned rules to minimize false positives while maintaining detection coverage.

---

## ⚔️ Simulated Attack Scenarios

| Technique | MITRE ATT&CK ID | Detection Method |
|---|---|---|
| Unauthorized Scheduled Task | T1053.005 | Sysmon Event ID 1 + Wazuh custom rule |
| Registry Run Key Persistence | T1547.001 | Sysmon Event ID 13 |
| Port Scan (Nmap) | T1595 | Suricata ET SCAN ruleset |
| SSH Brute Force | T1110.001 | Wazuh built-in + custom threshold rule |
| Event Log Clearing | T1070.001 | Sysmon Event ID 104 |
| Security Tool Tampering | T1562.001 | Wazuh FIM + process monitoring |

---

## 📁 Repository Structure

```
soc-homelab-wazuh-elk/
├── 📂 configs/
│   ├── 📄 wazuh_agent.conf          # Endpoint agent configurations
│   ├── 📄 suricata.yaml             # NIDS configuration
│   └── 📄 sysmon_config.xml         # Custom Sysmon ruleset (SwiftOnSecurity-based)
│
├── 📂 detection_rules/
│   ├── 📄 custom_wazuh_rules.xml    # Custom Wazuh rules (MITRE-mapped)
│   └── 📄 custom_suricata.rules     # Custom network signatures
│
├── 📂 attack_simulation/
│   └── 📄 auto_attack_gen.py        # Python wrapper for Atomic Red Team
│
├── 📂 screenshots/
│   ├── 📄 01_kibana_overview_dashboard.png
│   ├── 📄 02_wazuh_active_alert_privilege_escalation.png
│   ├── 📄 03_suricata_port_scan_alert.png
│   ├── 📄 04_sysmon_log_scheduled_task.png
│   └── 📄 05_elk_event_correlation.png
│
└── 📄 README.md
```

---

## 📸 Dashboards & Detection Showcase

### Kibana Overview Dashboard
> *Tổng quan toàn bộ log ingestion và alert trong 24h — Windows events, Linux syslog, Suricata alerts*

![Kibana Overview Dashboard](screenshots/01_kibana_overview_dashboard.png)

---

### Wazuh Active Alert — Privilege Escalation Detected
> *Script Python chạy Atomic Red Team kích hoạt rule T1053 — alert level 12 bật lên trên Wazuh Manager*

![Wazuh Active Alert](screenshots/02_wazuh_active_alert_privilege_escalation.png)

---

### Suricata — Port Scan Detection
> *Suricata bắt được port scan từ Kali Linux, EVE.json được đẩy về Wazuh và hiển thị trên Kibana*

![Suricata Port Scan](screenshots/03_suricata_port_scan_alert.png)

---

### Sysmon — Suspicious Scheduled Task (Event ID 4698)
> *Windows Event ID 4698 — Sysmon ghi nhận task tạo bởi script mô phỏng T1053.005*

![Sysmon Log](screenshots/04_sysmon_log_scheduled_task.png)

---

### ELK — Multi-source Event Correlation
> *Tương quan sự kiện từ nhiều nguồn: timeline từ port scan → lateral movement attempt → persistence*

![ELK Correlation](screenshots/05_elk_event_correlation.png)

---

## ⚙️ Quick Setup Guide

> ⚠️ *This repo contains configs and scripts only. VMs are not included.*

### Prerequisites
- VirtualBox or VMware
- 16GB RAM recommended (4 VMs running simultaneously)
- Host OS: Windows 10/11 or Linux

### VM Specs Used

| VM | OS | RAM | Role |
|---|---|---|---|
| SIEM-Core | Ubuntu 22.04 | 6GB | Wazuh Manager + ELK |
| Victim-Win | Windows 10 | 3GB | Sysmon + Wazuh Agent |
| Victim-Linux | Ubuntu 22.04 | 2GB | Wazuh Agent |
| Attacker | Kali Linux | 3GB | Atomic Red Team |

### Deploy Steps
1. Install Wazuh Manager on SIEM-Core: [docs.wazuh.com](https://documentation.wazuh.com/current/installation-guide/index.html)
2. Deploy ELK Stack alongside Wazuh
3. Copy `configs/wazuh_agent.conf` to each endpoint and register agents
4. Apply `configs/sysmon_config.xml` on Windows VM via Sysmon
5. Deploy Suricata on network-tap VM with `configs/suricata.yaml`
6. Import `detection_rules/custom_wazuh_rules.xml` into Wazuh Manager
7. Run `attack_simulation/auto_attack_gen.py` to validate detections

---

## 🎯 Skills Demonstrated

`Blue Team Operations` · `SIEM Configuration` · `Detection Engineering` · `Log Analysis` · `Network Security Monitoring` · `Adversary Emulation` · `MITRE ATT&CK Framework` · `Python Scripting` · `Incident Response Triage` · `Threat Hunting`

---

## 📚 References

- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Elastic SIEM Guide](https://www.elastic.co/guide/en/security/current/index.html)
- [Suricata User Guide](https://suricata.readthedocs.io/)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [SwiftOnSecurity Sysmon Config](https://github.com/SwiftOnSecurity/sysmon-config)

---

*Developed as a self-study initiative to deepen practical understanding of Blue Team operations, Detection Engineering, and Incident Response.*
