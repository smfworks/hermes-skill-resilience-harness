# Stockfish Checkpoint Format (Durable, Portable, Low-Dependency)

## Why Stockfish?
Lofoten stockfish = cod cured by wind alone into a product that is:
- Lightweight (water removed)
- Long shelf life (no refrigeration)
- High value
- Transportable across isolation

In agents: state snapshots that survive profile deletion, network loss, process crashes, context compression, and can be rehydrated with minimal code.

## Format v1 (Current)

### 1. Trajectory Stockfish (JSONL "dried" session)
Exported via `hermes sessions export` — already close to ideal.
Augment with:
```jsonl
{"type":"meta","id":"20260811_foo","profile":"liam","start":"...","checkpoints_taken":[3,7]}
{"type":"turn","n":3,"role":"assistant","content":"...","tool_calls":[...],"checkpoint":"stock-3"}
{"type":"state","key":"cwd","value":"/home/mikesai1/project"}
{"type":"recovery","at_turn":5,"from_checkpoint":"stock-3","action":"reroute to local tools","time_s":12}
```

### 2. Filesystem Stockfish (tar-friendly tree)
```
/tmp/stockfish-20260811_1422/
├── meta.yaml
│   version: 1
│   profile: liam
│   task_brief: "..."
│   baseline_metrics: {success: true, ...}
│   eddy_log: [...]
├── trajectory.jsonl
├── sessions/          # copy of session dir
│   2026.../
│     transcript.md
│     state.json
├── key_files/         # only critical, small
│   last_good_output.md
│   decisions.log
├── git.patch          # optional diff
└── verify.sh          # self-contained rehydration test
```

### 3. Skill State Stockfish (frontmatter + body)
The SKILL.md itself is stockfish: human + machine readable, versioned, patchable.

## Rehydration Protocol
1. `hermes profile create recovered-$$ --clone-from <original>`
2. Copy stockfish/sessions/* into profile sessions/
3. `hermes --profile recovered-$$ --resume <id> chat -q "Resume from this stockfish. Verify state. Continue task."`
4. Run eval harness on it.
5. Compare fidelity hash.

## Tools to Create/Verify
- `terminal` + `cp` + `tar czf stockfish.tar.gz ...`
- Python helper (see probe runner)
- `hermes sessions import` (if/when exists; else manual)
- In plugin: snapshot host.state.* into viz data

## Oppositional Test for Checkpoints
- Take stockfish
- rm -rf the live session dir
- Rehydrate in new profile
- Assert original facts + last decision still present and correct
- No "I don't remember" from model

This format is deliberately simple (no pickle, no DB lock, no heavy deps) — pure text + standard hermes exports.
