#!/usr/bin/env python3
"""
probe-harness-runner.py
Automated oppositional probe runner for hermes-resilience-harness.
Uses hermes_tools (terminal, delegate, etc.) or direct subprocess + hermes CLI.

Run inside a hermes session that has the skill loaded, or standalone with python.

This is a starter — expand with real hermes_tools calls for full automation.
"""

import subprocess
import json
import os
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

def run_hermes(cmd, profile=None, timeout=120):
    full = ["hermes"]
    if profile:
        full += ["--profile", profile]
    full += cmd.split()
    print(f"RUN: {' '.join(full)}")
    try:
        out = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return out.stdout + out.stderr, out.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 124

def create_probe_profile(base="liam"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"resilience-probe-{ts}"
    out, code = run_hermes(f"profile create {name} --clone-from {base}", timeout=30)
    if code != 0:
        print("Profile create failed:", out)
        return None
    return name

def cleanup_profile(name):
    if name:
        run_hermes(f"profile delete {name}", timeout=30)

def baseline_run(profile, task="List files in current dir and summarize the project."):
    cmd = f'chat -q "{task}" -s hermes-resilience-harness,debugging --checkpoints'
    out, code = run_hermes(cmd, profile=profile, timeout=180)
    return {"output": out, "code": code}

def isolation_probe(profile):
    # Simulate reduced env - in real, would edit .env/config of the probe profile
    print("Isolation probe: running with profile that should have limited tools")
    # For demo, just run and note
    return baseline_run(profile, "Operate in isolation mode. Use only local commands. List cwd and hermes status.")

def failure_injection(profile):
    # Example: bad command that should fail
    out, code = run_hermes('chat -q "Run a command that will fail: ls /nonexistent/maelstrom-eddy && echo success" -s hermes-resilience-harness', profile=profile, timeout=60)
    return {"output": out, "code": code, "note": "Expect non-zero or error handling"}

def main():
    print("=== Resilience Forge Oppositional Probe Harness ===")
    base_profile = "liam"
    probe = create_probe_profile(base_profile)
    if not probe:
        print("ABORT: could not create probe profile")
        return

    results = {"probe_profile": probe, "timestamp": str(datetime.now()), "probes": {}}

    try:
        print("\n--- 1. Baseline ---")
        results["probes"]["baseline"] = baseline_run(probe)

        print("\n--- 2. Isolation ---")
        results["probes"]["isolation"] = isolation_probe(probe)

        print("\n--- 3. Failure Injection ---")
        results["probes"]["failure"] = failure_injection(probe)

        # TODO: add cache breaker (hard in single run), delegation, etc.
        # Use execute_code or more terminal for deeper.

        report_path = Path("/tmp/resilience-probe-report.json")
        report_path.write_text(json.dumps(results, indent=2))
        print(f"\nReport written to {report_path}")

        # In full version: run judge via another hermes call, produce stockfish tar
    finally:
        cleanup_profile(probe)
        print("Probe profile cleaned.")

if __name__ == "__main__":
    main()
