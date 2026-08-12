# Lofoten Metaphors → Executable Code & Practices

This table is the bridge. Every resilience feature should have a clear "this comes from real Lofoten practice" rationale.

| Lofoten Reality | Agent Metaphor | Implementation in hermes-resilience-harness | Evidence / Test |
|-----------------|----------------|---------------------------------------------|-----------------|
| Fishing villages (rorbuer) prepare for winter storms with stockfish racks | Pre-task preparation & durable checkpoints | - Load minimal skill set + this harness at start of complex task<br>- `hermes --checkpoints`<br>- Custom `stockfish/` dir with compressed exports + state snapshots | Baseline run + `ls /tmp/stockfish-*` in probes |
| Moskstraumen eddies (tidal, shifting, powerful but navigable with local knowledge) | Workflow turbulence: tool loops, delegation stalls, context drift | - Eddy detection in eval harness (repeat count >2)<br>- maelstrom-viz visual currents<br>- Recovery playbook phases 1-5 | Oppositional failure injection + recovery time metric |
| Stockfish: air-dry cod, no salt, lightweight, survives months of isolation/transport | Minimal, portable, dependency-free state artifacts | - JSONL + MD "dried" trajectories (no runtime objects)<br>- Use Hermes compression only when needed<br>- Profile-isolated storage | Isolation probe: delete profile, re-import stockfish, resume |
| Isolated crews in small villages (self-sufficient, know their fjord) | Profile isolation + narrow skill loading | - `hermes profile create --clone-from` for probes<br>- Test with net/tools disabled<br>- Skills declare required envs explicitly | Cross-profile read attempt fails or is audited; `hermes doctor` clean in isolated profile |
| Fleet of boats coordinate via signals/stories without central control | Delegation + cross-profile handoff with verification | - Explicit brief + return-evidence contract<br>- Parent verifies child output against stockfish<br>- Saga memory for narrative handoffs (sister skill) | Delegation stress probe (3-chain with kill) |
| Right to roam (allemannsretten) + responsibility (no trace, respect nature) | Bounded, auditable, sustainable agent actions | - Prefer skills/plugins (edge) over core tools (per AGENTS.md)<br>- Log all file/terminal/net changes<br>- "Leave no trace" cleanup in recovery | E2E test leaves working dir clean; audit log in vault |
| Dramatic light (midnight sun / polar night) + rapid weather change | Variable conditions: model drift, rate limits, provider weather | - Adaptive fallback in recovery (local model, cached data)<br>- Verifier always runs deterministic first<br>- Status chips show "weather" | Resource weather probe (auth reset, simulated 429) |
| Cod spawning runs (massive, seasonal, predictable with knowledge) | Predictable high-value workflows instrumented | - Trajectory harness captures "spawning" (peak activity) metrics<br>- Pre-loaded for known tasks | Metrics show high catch-value on repeated tasks |
| Community craft: precision in boat-building, patience in drying | Quality bar for releases | - Oppositional 7-probe suite mandatory<br>- Fleet sign-off (independent 2nd crew run)<br>- Evidence in GitHub + vault before publish | This skill + plugin passed its own probes during creation |

## Mapping to AGENTS.md Principles
- Narrow waist: reinforced by "village self-reliance" = don't bloat core.
- Prompt caching sacred: "do not disturb the drying racks" = no mid-convo mutations.
- E2E validation over mocks: "test in the real fjord weather", not sheltered harbor.
- Behavior contracts: "the crew's word is the dried stockfish — verifiable facts".

## How to Use This Table
When adding a feature to any skill/plugin:
1. Pick 1+ row.
2. Implement the "Implementation" column.
3. Add a probe that exercises the metaphor.
4. Document in the feature's own references with link back here.
5. Update this table if new pattern discovered.

## From the 2026-08-11 Challenge
- Resilience Forge Team used "village preparation" to mkdir + write references before coding plugin.
- Used "stockfish" for all created files (portable MD).
- "Eddy" probes applied to own creation (edits while running, isolation via profile).
- Maelstrom viz chosen to make the metaphor visible in UI.

This is living substrate. Patch when new real Lofoten insight applies to agents.
