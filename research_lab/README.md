# Codex × Gemini Mathematical Research Lab

This directory automates the research loop that was previously being done manually:

1. Gemini independently tries to construct/prove/refute the current claim.
2. Codex independently attacks the same claim adversarially.
3. Each receives the other's independent report and responds.
4. A Codex adjudicator produces a structured verdict.
5. The next round targets only the obligations that survived.

The loop is designed to reduce **social convergence** between models: the independent first pass happens before either model sees the other model's conclusion.

## Safety model

- Codex runs with a **read-only sandbox**.
- Gemini runs with `--approval-mode=plan` and a prompt that forbids leaving Plan Mode or modifying files.
- No agent is allowed to push, merge, delete, or edit the official manuscript.
- Runtime artifacts are local and ignored by Git by default.
- An automated `PROVED` verdict means only **candidate for human review**. It does not update `CERTIFIED_FACTS.md`.

## Requirements

On Windows, from PowerShell:

```powershell
codex --version
gemini --version
python --version
```

Recommended Python: 3.11+; the project currently uses Python 3.13/3.14.

Codex must already be authenticated. Gemini CLI must already be authenticated.

Current Codex non-interactive mode uses `codex exec`. The lab invokes it with a read-only sandbox and JSON/JSON-schema output.

Current Gemini CLI headless mode uses `gemini -p ...`. The lab invokes it with Plan Mode and JSON output.

## First run

Checkout this branch, then:

```powershell
git checkout codex/math-research-lab
python .\research_lab\doctor.py
.\research_lab\run.ps1
```

Or:

```powershell
python .\research_lab\orchestrator.py
```

The default run performs up to the number of rounds configured in `config.toml`.

## What gets written locally

```text
research_lab/
  rounds/
    001/
      codex_independent.md
      gemini_independent.md
      codex_cross_review.md
      gemini_cross_review.md
      adjudication.json
      codex_events.jsonl
      ...
  runtime/
    WORKING_STATE.md
    LATEST_VERDICT.json
    RUN_STATUS.json
```

These directories are ignored by Git so that research transcripts do not pollute the repository unless you intentionally add them.

## Stop conditions

The orchestrator stops when any of the following occurs:

- exact refutation with a certificate;
- two consecutive adjudications return `PROVED` with no surviving obligations;
- the obligation set does not change for the configured number of rounds;
- Codex or Gemini is unavailable/quota-limited;
- timeout;
- maximum number of rounds.

Even after an automatic stop on `PROVED`, human review remains mandatory.

## Current focus

See `CURRENT_CLAIM.md`.

At the time this lab was initialized, the M6 construction gives a rigorous upper bound

```text
m_{*,HT}^{mult} <= 6
```

for linear 3-uniform hypertrees, while the claimed equality `= 6` remains under adversarial audit. The latest Gemini “Egorov–Liouville cascade” and disjoint-pair second-moment arguments are deliberately stored as **claims to audit**, not automatically certified facts.

## Resume

The orchestrator detects existing numeric round directories and continues with the next number. It also reads `runtime/WORKING_STATE.md` when available.

To start clean locally, remove only:

```powershell
Remove-Item -Recurse -Force .\research_lab\rounds\*
Remove-Item -Recurse -Force .\research_lab\runtime\*
```

Do not delete the static state files.
