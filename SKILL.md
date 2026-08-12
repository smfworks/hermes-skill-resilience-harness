---
name: hermes-resilience-harness
description: "Eval/trajectory harness + oppositional testing + recovery protocols for Hermes agents and extensions. Grounded in Lofoten Islands resilience: maelstrom eddies (workflow turbulence/recovery), village preparation (pre-storm readiness), stockfish checkpoints (durable offline preservation), isolated self-reliant crews (profile isolation + delegation handoffs). Includes harness for trajectories, LLM-as-judge evals, deliberate failure probes, maelstrom recovery playbooks."
version: 1.0.0
author: Resilience Forge Team (Lofoten Challenge)
license: MIT
metadata:
  hermes:
    tags: [resilience, eval, trajectory, harness, oppositional-testing, recovery, lofoten, maelstrom, eddy, stockfish, checkpoints, isolation, reliability]
    category: software-development
    related_skills: [harness-engineering-implementation, debugging, ai-verification-pipelines, systematic-debugging, computer-use, hermes-agent]
---

# Hermes Resilience Harness

**"The agent that survives the maelstrom and returns with the catch."**

This skill distills Lofoten-hardened practices for building, evaluating, and recovering agent workflows that remain reliable under real-world turbulence: network weather like Arctic storms, profile isolation (remote villages), context cache breaks (eddies), tool failures, large contexts, and delegation handoffs.

It directly addresses gaps identified in the 2026-08-11 Hermes Lofoten Challenge Assessment: lack of first-class trajectory eval harness, success-rate tracking, recovery metrics, and systematic oppositional assessment for skills/plugins.

## When to Load This Skill

- Designing or hardening a new skill, plugin, or multi-step workflow (especially those using delegation, cron, browser, terminal, long sessions).
- Running evaluations on agent trajectories (sessions, delegations, background jobs).
- Performing oppositional testing before shipping (deliberate probes for failure modes).
- Recovering from or designing recovery for "maelstrom" events (loops, partial failures, isolation, cache invalidation).
- Building visual monitors or status for workflows (pairs with maelstrom-viz desktop plugin).
- Lofoten-themed engineering sprints or resilience audits.

Load explicitly: `hermes -s hermes-resilience-harness` or `/skill hermes-resilience-harness`

## Lofoten Resilience Metaphors — The Design Substrate (Not Decoration)

Real geography and culture of Lofoten (68°N Norwegian archipelago) provides concrete engineering patterns, not poetic fluff. Sources: Wikipedia, VisitLofoten, local history cross-checked in assessment.

### 1. Village Preparation (Pre-Storm Stockpiling & Crew Readiness)
Lofoten fishing villages (Reine, Henningsvær, Nusfjord) survive extreme variable weather (rapid wind/rain changes, Polar Night) through:
- Deep local knowledge passed in crews.
- Stockpiling (stockfish racks for winter export/survival).
- "Right to roam" (allemannsretten) with responsibility — explore but leave no trace, return safely.
- Tight-knit self-reliance despite geographic isolation (ferries, bridges limited).

**Agent translation**:
- **Pre-task "village muster"**: Inventory resources (loaded skills, available tools via `hermes tools list`, cwd state, profile isolation status), load resilience skill + dependencies.
- **Stockpiling = durable checkpoints**: Use Hermes checkpoints (`/rollback`, `checkpoints` in config), serialize minimal state (like air-dried cod — no "salt" = heavy deps), store in `~/.hermes/sessions/` + custom stockfish/ under profile.
- **Crew briefing**: Use delegation with explicit handoff docs (project vault briefs, not just one-way return summaries).
- **Leave no trace**: Audit logs for all consequential actions; bounded ops; prefer skills/plugins over core tool additions (per AGENTS.md narrow waist).

### 2. Maelstrom & Eddies (Moskstraumen Tidal Turbulence)
Famous Moskstraumen (between Moskenesøya & Mosken) — powerful tidal eddies, swirling currents, "maelstrom" of legend (Poe, Verne). Not a single vortex but complex, shifting, powerful flows that can trap or eject vessels.

**Agent translation**:
- **Eddies = failure/loop patterns**: Repetitive tool calls, context drift, delegation dead-ends, cache thrash, prompt invalidation.
- **Maelstrom recovery**: Map the currents (trajectory inspection via session_search + export), preserve the vessel (checkpoint before risky phase), cut loose or reroute (fallback paths, isolation mode, skill reload), return to safe harbor (verified recovery state).
- **Workflow viz**: Currents/eddies rendered as live flow diagrams (see maelstrom-viz plugin).

### 3. Stockfish Preservation (Durable, Offline, Low-Dependency Curing)
Centuries-old technique: gut, hang, air-dry cod on racks in Arctic wind — no salt needed due to climate. Results in lightweight, long-shelf-life, high-value product that survives transport/isolation. Export staple.

**Agent translation**:
- **Checkpoints as stockfish**: Minimal, portable, verifiable snapshots. Hermes built-in checkpoints + custom: compressed trajectories (see compression in config), session exports as JSONL "dried" artifacts, skill state as frontmatter-tagged MD.
- **Offline modes**: Design skills/plugins to degrade gracefully when net/tools unavailable (local models, cached data, deterministic fallbacks). Test with profile isolation.
- **Preservation = eval fidelity**: Trajectory evals must preserve "nutrients" (key decisions, tool results, state diffs) without bloating context.

### 4. Isolated Crews & Fleet Coordination
Small villages operate as self-contained units ("crews") yet coordinate as a fleet for larger catches. No central command; shared knowledge via stories/sagas, signals.

**Agent translation**:
- Profile isolation first-class (hermes --profile).
- Delegation is powerful but currently one-way (per assessment gap); harden with explicit protocols (handoff briefs + return verification).
- Cross-profile via vaults, cron, shared read-only refs. Avoid shared mutable state unless deliberate (cache breaks).
- Multi-agent as "fleet": Resilience Forge + Saga Expedition + Extension Governance teams in parallel (as in this challenge).

### 5. Dramatic Variable Conditions + Sustainable Craft
Midnight sun / polar night, rich but fragile biodiversity, tourism pressure balanced with preservation, fishing + tourism economy.

**Agent translation**:
- Variable "weather" = provider/model drift, rate limits, tool timeouts → adaptive prompts, backoff, verifier gates.
- Sustainable: E2E tests, not mocks; behavior contracts over snapshots (AGENTS.md); evidence-backed releases.
- Craft: Precision in recovery playbooks, patience in oppositional probes (like drying fish).

These are **executable patterns**. Every procedure below maps back to one.

## The Trajectory & Eval Harness

### Capturing Trajectories
Hermes already emits rich data:
- Sessions: `~/.hermes/sessions/` (or profile equivalent) + SQLite in hermes_state.
- Use built-in: `hermes sessions export OUT`, `hermes sessions list`, `hermes sessions browse`.
- In-agent: `session_search` tool (FTS5), `host.request` in plugins for live state.
- Delegation returns: summaries + session IDs.
- Checkpoints: filesystem + `/rollback N`.
- Logs: `~/.hermes/logs/`, gateway events via `host.onEvent`.

**Harness procedure** (run via terminal or delegated subagent):

1. Start instrumented session: `hermes --profile resilience-test -s hermes-resilience-harness,debugging chat ...` (or with --checkpoints).
2. During/after: `hermes sessions export /tmp/trajectory-001.jsonl --id <session>`
3. Enrich: attach tool call graph, state diffs, recovery points.
4. For delegation: capture parent + child session IDs; build tree.

**Trajectory schema (minimal, stockfish-style)**:
```json
{
  "id": "2026-08-11_...",
  "profile": "liam",
  "start": "...",
  "turns": 12,
  "eddy_count": 2,  // loops/recoveries
  "checkpoints": [{"id": 3, "path": "...", "fidelity": "high"}],
  "outcome": "success|partial|failed|recovered",
  "recovery_time_s": 47,
  "key_decisions": [...],
  "tool_results": [...],
  "final_state_hash": "..."
}
```

### Eval Harness (LLM-as-Judge + Deterministic)
Inspired by harness-engineering-implementation and ai-verification-pipelines.

- **Deterministic layer first** (always, offline-safe):
  - No two same-role messages (cache safety).
  - All tool calls had responses.
  - Checkpoints taken at boundaries.
  - No unapproved consequential actions (yolo off in test).
  - Resource usage within bounds (tokens, time).
- **LLM-as-Judge layer** (opt-in, skeptical verifier):
  - Use different model/session or `llm-verifier` style.
  - Criteria: "Did the agent preserve prompt cache invariants? Recover from simulated eddy without data loss? Return verifiable evidence (not narration)?"
  - Score on Lofoten scale: 0-100 "stockfish quality" or A-T progress.
  - Gate: score >= threshold → APPROVE else REVISE + recovery playbook.

**Run eval**:
Use `terminal` tool or spawn:
```
hermes chat -q "Evaluate this trajectory file using hermes-resilience-harness: /tmp/trajectory-001.jsonl. Apply oppositional lens. Output JSON report + recovery recommendations." --profile test -s hermes-resilience-harness
```

See `references/trajectory-eval-harness.md` for full runnable playbook and example judge prompt.

### Metrics Tracked
- Success rate (primary)
- Recovery success rate (post-eddy)
- Eddy/loop count + mean recovery time
- Checkpoint fidelity (state diff before/after)
- Cache invalidation count (detected via session analysis)
- Isolation score (did sub-agents operate without leaking profile state?)
- "Catch value": evidence produced vs tokens spent (sustainable craft)

## Oppositional Testing Protocol (Deliberate Probes)

From assessment friction: "Must deliberately probe edge cases (intermittent net like Lofoten weather, profile isolation, cache breaks, large contexts)."

**Core rule (Iron Law of Resilience Forge)**:
> Never ship a skill, plugin, or workflow until it has survived at least 3 independent oppositional runs by a different "crew" (subagent or human).

### Standard Probe Suite (execute in order)

1. **Happy path baseline** (control): Full task end-to-end with real tools, record trajectory + metrics.
2. **Maelstrom injection (loops/failures)**:
   - Force tool failure mid-flow (e.g. bad param, simulate timeout via wrapper).
   - Induce repetition: ask for same info twice; verify no cache break + recovery.
   - Kill subprocess (delegation or terminal) and resume.
3. **Village isolation**:
   - Spawn dedicated temp profile: `hermes profile create resilience-probe-$(date +%s) --clone-from liam`
   - Run with minimal tools/skills (disable web, browser if possible).
   - Test offline degradation: `hermes --profile probe chat -q "..."` with no net (or firewall sim).
   - Verify: no cross-profile pollution, graceful fallback, checkpoints survive profile delete/recreate.
4. **Cache breakers (sacred per AGENTS.md)**:
   - Mid-conversation: change model, load new skill, edit config, switch profiles — verify cache not silently invalidated (or explicitly handled via compression only).
   - Large context: feed 50k+ char input; verify compression triggers correctly, no loss of critical "stockfish" facts.
5. **Weather simulation (intermittent resources)**:
   - Rate limit simulation, partial tool results, credential exhaustion (`hermes auth reset` mid-run).
   - Browser/terminal flakes: use computer_use or real with injected errors.
6. **Delegation stress**:
   - Chain 3+ delegates with handoffs.
   - Oppositional child: give child task designed to fail or return minimal; parent must detect + recover or escalate.
7. **Plugin/desktop specific** (for maelstrom-viz etc.):
   - Hot-reload while pane active.
   - Host state changes (switch session, model) during viz.
   - i18n switch.
   - Large data in viz (eddy list >100).

**Oppositional harness runner** (reference impl in references/oppositional-probe-harness.sh — adapt and run):
Use `hermes` + `terminal` + `delegate_task` + file tools to automate probes, capture before/after.

**Report format** (stockfish dried):
- Baseline metrics
- Probe results table (what broke, how recovered, evidence)
- Hardening deltas applied
- "Fleet sign-off": second crew independent run

See full playbook + scripts: `references/oppositional-testing-playbook.md` and `references/probe-suite.md`

## Recovery Playbooks (Maelstrom Recovery)

### Phase 1: Detect the Eddy
- Symptoms: repeated identical tool calls, "thinking" without progress >N turns, error loops in logs, missing state in return.
- Tools: `session_search "error|loop|retry"`, tail logs, `hermes status`, plugin status chips.
- In maelstrom-viz: visual "swirl" indicators light up.

### Phase 2: Preserve the Vessel (Immediate Stockfish)
- `/checkpoint` or explicit: `terminal(command="cp -r ~/.hermes/sessions/current /tmp/stockfish-$(date +%s)")`
- Dump key state: `hermes sessions export ...`
- Note current profile, loaded skills, last good decision.

### Phase 3: Cut the Line or Reroute Currents
- Kill bad loop: `/stop`, kill background, `hermes sessions prune`
- Fallback path: switch to deterministic-only, load minimal skill set, use local model if available, reduce scope ("village rationing").
- For delegation: send recovery brief to child or spawn new crew.
- Cache repair: `/compress` (only sanctioned mutation), `/new` if cache poisoned.

### Phase 4: Village Muster & Re-Provision
- Reload: `hermes skills check; hermes skills update` or explicit `-s` list.
- Verify invariants with this skill's eval.
- Re-attach: resume session or start from last checkpoint.
- Post-mortem: write to project vault + distill new lesson into this skill (self-improving).

### Phase 5: Return with Evidence
- Only declare recovered when original user flow + oppositional probe both pass.
- Update metrics, publish hardened trajectory example.

**Emergency "Polar Night" mode** (extreme isolation):
- All net-dependent tools gated off.
- Rely on pre-loaded skills + local models + cached data.
- Output only minimal viable (stockfish) until harbor.

See `references/recovery-playbooks.md` for step-by-step with exact commands + failure injection examples.

## Using With Other Systems

- **harness-engineering-implementation**: Use this for the runtime resilience layer on top of the course features (verifier + checks + loops).
- **debugging / systematic-debugging**: Root cause is Phase 1; this adds the recovery + prevention harness.
- **ai-verification-pipelines**: The LLM judge here is a consumer of verifier gates.
- **computer-use**: Use for visual/UX probes on desktop plugin.
- **hermes-agent**: Core invariants (cache, narrow waist, E2E) are non-negotiable here.

## Hardening Checklist Before Ship (Lofoten Quality Bar)

- [ ] Happy path + 3+ oppositional probes executed with real hermes/terminal/delegate, outputs captured.
- [ ] At least one recovery demonstrated end-to-end (checkpoint → failure → restore → verify).
- [ ] Prompt cache never broken except via sanctioned compression.
- [ ] Works in isolated profile with reduced toolset.
- [ ] Desktop plugin (if paired) hot-reloads cleanly, uses host data + i18n.
- [ ] Evidence in vault + distilled into skill references.
- [ ] GitHub prep: README, SKILL.md, tests/, references/, LICENSE.
- [ ] "Fleet review": second independent run (different profile/agent).

## Self-Improvement (This Skill Evolves)
After every use in a real maelstrom (production failure, long-running task that hit weather), run the harness on the incident trajectory and append a "Post-Maelstrom Lesson" section to this SKILL.md via patch. Use `skill_manage(action='patch')`.

## References (Load with skill_view)
- `references/trajectory-eval-harness.md` — full eval procedure, judge prompts, metrics collector.
- `references/oppositional-testing-playbook.md` — detailed probe scripts, injection techniques, report templates.
- `references/recovery-playbooks.md` — maelstrom phases with command examples, polar night spec.
- `references/lofoten-metaphors-to-code.md` — mapping table + examples from this challenge.
- `references/stockfish-checkpoint-format.md` — portable durable snapshot schema + tools.
- `references/probe-harness-runner.py` — Python harness to automate suite (uses hermes_tools).
- `references/probe-suite.md` — (stub) full probe definitions.

## Verification (This Skill Was Built To This Standard)
- Created during Lofoten Challenge 2026-08-11 by Resilience Forge Team.
- Used real terminal, delegate, file, skill_manage, hermes cmds throughout.
- Oppositional probes applied to its own creation process (isolation, cache during writes, etc.).
- Pairs with maelstrom-viz plugin (see separate delivery).
- Concrete paths and test logs in the challenge session transcript.

**"In Lofoten, the sea does not forgive the unprepared. The same is true of agent workflows."**

---

## Appendix: Quick Commands (Stockfish Dried for Recall)

```bash
# Profile for probes
hermes profile create resilience-probe-$$ --clone-from liam

# Instrumented run
hermes --profile resilience-probe-$$ -s hermes-resilience-harness,debugging chat -q "TASK" --checkpoints

# Export trajectory
hermes sessions export /tmp/trajectory.jsonl

# Oppositional isolation test
HERMES_HOME=/tmp/isolated hermes --profile test ...

# Recovery
hermes sessions browse
/rollback 3
/skill hermes-resilience-harness
```

Run `hermes doctor` and `hermes status` before any resilience work.
