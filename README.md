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
│
└── 📄 README.md
```

---

## 📸 Dashboards & Detection Showcase

### Atomic Red Team run test 

<img width="1010" height="1012" alt="image" src="https://github.com/user-attachments/assets/5462772d-a8c8-433a-860a-f21b41aa7b57" />

### Wazuh Overview Dashboard

<img width="1624" height="963" alt="image" src="https://github.com/user-attachments/assets/bed4b5ce-09f6-4192-a2c9-cefc06e60e1b" />

<img width="1650" height="779" alt="image" src="https://github.com/user-attachments/assets/4345a532-37b2-4533-8449-a7e6c3143302" />

### Sysmon Alert

<img width="1635" height="737" alt="image" src="https://github.com/user-attachments/assets/e98cfaf6-865e-4d8e-8cb8-25fe51fcc1f3" />

<img width="1650" height="926" alt="image" src="https://github.com/user-attachments/assets/d93181f6-0a31-40e6-bd17-85fe4f32ca97" />

---

## ⚙️ Quick Setup Guide

> ⚠️ *This repo contains my sample configs and scripts only. VMs are not included.*

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
