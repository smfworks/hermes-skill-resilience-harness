# Trajectory Eval Harness — Detailed Playbook

## Purpose
Capture, normalize, score, and report on Hermes agent sessions/trajectories using deterministic + LLM-judge layers. Produce "stockfish" artifacts: lightweight, verifiable, preservable.

## Prerequisites
- hermes-resilience-harness loaded
- Access to `hermes sessions`, `session_search`, `terminal`, `file` tools
- (Optional) `ai-verification-pipelines` or llm-verifier for judge

## Step-by-Step Procedure

1. **Instrument the Run**
   ```bash
   hermes --profile <probe> -s hermes-resilience-harness,debugging,ai-verification-pipelines \
     chat -q "YOUR TASK HERE. Use checkpoints." \
     --checkpoints -v
   ```
   Note the session ID from output or `hermes sessions list`.

2. **Capture Raw Trajectory**
   ```bash
   hermes sessions export /tmp/trajectory-$(date +%s).jsonl --id <SESSION_ID>
   # Also:
   cp -r ~/.hermes/profiles/<profile>/sessions/<id> /tmp/stockfish-raw/
   ```

3. **Enrich (Deterministic Analysis)**
   Use code_execution or Python in terminal to parse JSONL:
   - Count turns, tool calls, errors.
   - Detect eddies: sequences of >2 identical assistant messages or tool repeats.
   - Extract checkpoints taken.
   - Compute basic metrics (see below).

4. **LLM Judge Pass (Skeptical Verifier)**
   Delegate or run:
   ```bash
   hermes chat -q "
   You are a skeptical Lofoten village elder judging a fishing expedition (agent trajectory).
   Read the full trajectory JSONL below. Score 0-100 on:
   - Preparation (did it load right skills, take checkpoints?)
   - Maelstrom handling (eddies detected/recovered?)
   - Stockfish quality (evidence returned vs narration? durable state preserved?)
   - Isolation discipline (no leaks, cache safe?)
   - Overall catch value.
   Output strict JSON: {score, eddy_count, recovery_count, evidence_quality, verdict: 'APPROVE'|'REVISE'|'FAIL', recommendations: [...] }
   TRAJECTORY:
   $(cat /tmp/trajectory-....jsonl)
   " -s hermes-resilience-harness --profile judge
   ```

5. **Produce Report + Stockfish Artifact**
   - Write /tmp/reports/trajectory-<id>-eval.md with scores + excerpts.
   - Minimal dried JSON for preservation.
   - Distill any new pattern back into SKILL.md or new reference.

## Metrics Definitions
- **success**: final answer verifiable against task (not just "done").
- **eddy_count**: loops > threshold.
- **recovery_time**: turns or seconds from first failure signal to stable progress.
- **fidelity**: % of pre-eddy state present post-recovery (diff tool).
- **cache_breaks**: count of mid-session toolset/skill/model changes (should be 0 except compress).
- **isolation_score**: 0-1 (sub-processes used only declared profile paths).

## Example Judge Prompt Template (in skill)
(See SKILL.md main for embedded.)

## Integration with Desktop
maelstrom-viz can poll or receive events for live "current strength" = recent eddy score.

## Hardening Notes from Lofoten Challenge
- Always capture before oppositional probe.
- Judge must be on separate profile or model to avoid self-grading bias.
- Store reports in project vault + GitHub for evidence.

Last updated: 2026-08-11 Resilience Forge.
