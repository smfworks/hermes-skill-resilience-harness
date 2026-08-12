# Oppositional Testing Playbook for Hermes Extensions

**"Test as if the maelstrom is coming — because in production it will."**

## Philosophy
Oppositional = adversarial but constructive. We deliberately break the system in controlled ways that mirror Lofoten conditions (sudden storms = rate limits/failures; isolation = profile/net loss; eddies = loops; cache fragility).

Goal: surface weaknesses before user does. Every probe must have a corresponding hardening.

## The 7 Probe Classes (Mandatory for v1.0+ skills/plugins)

### 1. Baseline (Control)
Run full task with all features. Record trajectory, metrics, video/screenshot if UI.
Success criteria: clean run, good metrics.

### 2. Failure Injection (Maelstrom Eddies)
- Tool timeout: wrap terminal calls or use bad args.
- Partial results: e.g. browser returns truncated.
- Process kill: `pkill -f hermes` or kill specific PID from `ps`, then resume with session ID.
- Loop induction: "Repeat the last step until I say stop" — observe detection.

**Command pattern**:
```bash
timeout 10s hermes --profile probe chat -q "task that will timeout" || echo "injected timeout"
```

### 3. Profile Isolation (Village Self-Reliance)
```bash
hermes profile create opp-isolate-$$ --clone-from liam
# edit the new profile's .env and config.yaml to strip net creds, disable web/browser if possible
hermes --profile opp-isolate-$$ -s hermes-resilience-harness chat -q "task requiring tools"
# verify: no access to original profile files, graceful degradation messages, checkpoints in isolated dir
hermes profile delete opp-isolate-$$
```

Test cross-profile leakage: attempt to read other profile's MEMORY.md etc. Should fail or be empty.

### 4. Cache & Context Breakers (Sacred Cow)
- During active chat (use tmux or two terminals):
  - `hermes config set model.default other-model`
  - Load new skill mid-flow via command.
  - Edit large file being read.
  - Force compression mid-task.
- Verify: conversation continues without "I forgot" or doubled messages. Check token accounting.
- Large context test: paste 100k char synthetic doc + ask precise question from end.

**AGENTS.md rule enforcement**: If any probe invalidates cache unintentionally, that's a bug to fix in the extension, not the test.

### 5. Resource Weather (Intermittent like Lofoten Storms)
- Credential: `hermes auth reset PROVIDER` then run.
- Rate: use `sleep` wrappers or known slow endpoints.
- Disk: fill /tmp partially, run large export.
- Memory: large file reads.

### 6. Delegation Fleet Stress
Use `delegate_task` tool (from autonomous-ai-agents or core).
- Child task designed to eddy: "do X but fail on step 3, return partial".
- Parent must: detect via return summary, decide recover/delegate-retry/escalate.
- Chain: A -> B -> C, kill B mid, see if A recovers or reports correctly.
- Handoff quality: child receives full brief? Parent verifies return evidence.

### 7. Hot-Reload & Live State (For Plugins)
For desktop plugins:
- Edit plugin.js while app running + pane visible.
- Change host data source.
- Switch i18n locale.
- Feed large eddy list (100+ items).
- Disable/enable in Settings → Plugins.

Use `computer_use` tool or manual: capture, edit, reload via ⌘K "Reload desktop plugins", re-capture.

## Automated Harness (Runner)
See `references/probe-harness-runner.py` (to be implemented in this harness).
It orchestrates via execute_code / terminal:
- Spawns profiles
- Runs probes in sequence
- Captures outputs
- Runs judge
- Produces summary report
- Can be scheduled via cron for regression.

## Report Template
```markdown
## Oppositional Report for <extension> <version>
Date: ...
Crew: Resilience Forge (probe profile: xxx)
Baseline: success, metrics=...
Probe 2 (failures): broke on Y, recovered via Z in 12s. Evidence: ...
...
Verdict: HARDENED / NEEDS WORK
Changes: patch applied to ...
```

## Lofoten Tie-In
Just as a rorbu (fishing cabin) is secured before a storm and crew knows every eddy in the local fjord, your extension must have been through the probes. Unprobed = not shippable.

## Evidence from This Build
During creation of hermes-resilience-harness itself:
- Used isolated writes.
- Multiple file ops + skill_manage under load.
- Tested cache by editing while "in session" (this transcript).
- Delegation planned for team.

All probes logged in session.

Last hardened: 2026-08-11
