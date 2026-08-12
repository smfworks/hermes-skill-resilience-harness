# Maelstrom Recovery Playbooks

## Overview
Recovery is not "retry". It is deliberate: preserve, diagnose, reroute, verify, distill.

Maps directly to Lofoten:
- Storm hits (eddy forms)
- Secure the boat and catch (stockfish checkpoint)
- Wait out or sail around (fallback)
- Return to village, repair, share story (muster + update skill)

## Universal Recovery Sequence (5 Phases)

### Phase 0: Prevention (Village Preparation)
- Always start with: load this skill + debugging.
- Take checkpoint at start of risky phase: `terminal "mkdir -p /tmp/stockfish/$(date +%s); cp ~/.hermes/... /tmp/..." ` or use built-in.
- Declare "weather report": current profile, tools enabled, known risks.

### Phase 1: Detect Eddy (Early Warning)
Signals:
- >2 identical consecutive assistant outputs or tool calls.
- Error rate spike in logs: `tail -f ~/.hermes/logs/gateway.log | grep -E 'error|timeout|failed'`
- Session search: `session_search query="retry|again|failed" role=assistant`
- Status: `hermes status --all`
- Visual: maelstrom-viz shows swirl count rising, status chip red.

Action: **STOP** the loop immediately (`/stop` or kill PID).

### Phase 2: Secure Stockfish (Preserve Evidence & State)
```bash
TS=$(date +%Y%m%d_%H%M%S)
STOCK=/tmp/stockfish-$TS
mkdir -p $STOCK

# Export current session
hermes sessions export $STOCK/trajectory.jsonl

# Copy active session dir (profile aware)
PROFILE_DIR=$(hermes config path | xargs dirname)  # or known
cp -r $PROFILE_DIR/sessions/* $STOCK/sessions/ 2>/dev/null || true

# Key state snapshot
hermes status > $STOCK/status.txt
hermes tools list > $STOCK/tools.txt
cat ~/.hermes/MEMORY.md > $STOCK/memory.md 2>/dev/null || true

# Git state if in repo
git status --porcelain > $STOCK/git.txt || true

echo "Stockfish secured at $STOCK"
```

Also: note last good user-visible output + evidence.

### Phase 3: Cut Loose & Reroute (Survive the Swirl)
Options (escalate from least to most disruptive):

1. **Soft reroute**:
   - `/retry` (if last was transient)
   - Switch to simpler path: "Ignore previous, do only step X using only local tools"
   - Load fallback skill set: `-s hermes-resilience-harness,debugging` (no web)

2. **Medium**:
   - `/compress` (only allowed context mutation)
   - Resume from last checkpoint: `/rollback 2`
   - Spawn fresh sub-crew: delegate with "Recover from this stockfish: $STOCK. Original task: ..."

3. **Hard reset (Polar Night survival)**:
   - `/new`
   - New profile for clean isolation.
   - Reduce ambition: "Provide minimal viable output from known facts only. No new tool calls."

4. **Delegation recovery**:
   - Child returned garbage? Parent: "Your last response was eddy. Here is secured stockfish from before. Re-execute from there and return ONLY new evidence."

### Phase 4: Village Muster & Verify (Rebuild Trust)
- Re-provision: `hermes skills list; hermes doctor`
- Re-load harness.
- Run mini-eval on recovered trajectory vs stockfish.
- Execute original user request from the preserved state.
- **Evidence requirement**: Must produce the same (or better) verifiable artifacts as baseline. Narration alone = fail.

### Phase 5: Return + Distill (Self-Improve)
- Write incident report to vault: `~/<project>/incidents/maelstrom-$(date).md`
- Patch this skill: add "Post-Maelstrom Lesson: <date> <what broke> <fix>"
- Use `skill_manage(action='patch' ...)` 
- If plugin: hot-reload test.
- Update metrics in report.

## Specific Playbooks

### A. Tool Loop Eddy
Example: browser keeps clicking same element.
Recovery:
1. Stop.
2. Stockfish (note the bad selector in log).
3. Reroute: "Use different approach: terminal curl or search instead of browser for this data."
4. Verify new path succeeds.
5. Add to skill: "If X tool flakes, prefer Y."

### B. Delegation Black Hole
Child never returns or returns empty.
Recovery:
- Timeout on delegate (use tool timeout).
- Parent logs "child eddy suspected", spawns parallel second child with reduced scope + stockfish brief.
- On return, cross-verify outputs.
- Harden: require child to echo back key facts from brief.

### C. Cache Poison (Forbidden but happens)
Symptoms: model "forgets" earlier facts mid long convo.
Recovery:
- Immediate: `/compress` or `/new` + re-inject critical from stockfish (do not rely on poisoned context).
- Never mutate past messages.
- Post: file bug against core if AGENTS.md violated. Extension must not trigger it.

### D. Profile/Net Isolation Storm
Recovery:
- Detect: tool errors "connection refused", "no such file in other profile".
- Switch to pre-cached/local only.
- Output: "Operating in Polar Night mode. Using stockfish from <time>. Limited to ..."
- When harbor: re-sync, verify no permanent loss.

## Post-Recovery Checklist
- [ ] Original task completed with evidence.
- [ ] Oppositional probe re-run on hardened version passes.
- [ ] Stockfish archived to long-term (e.g. git + vault).
- [ ] Lesson added to this skill.
- [ ] maelstrom-viz status updated if applicable.

## Lofoten Example
A boat caught in Moskstraumen: secure lines (checkpoint), read the water (trajectory), wait for slack tide or motor out on known safe bearing (reroute using local knowledge = skill), return to rorbu, repair net, tell story over stockfish dinner (distill to crew knowledge).

**Never abandon the catch without securing it first.**

See also: references/lofoten-metaphors-to-code.md
