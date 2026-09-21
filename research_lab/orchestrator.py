#!/usr/bin/env python3
"""Codex × Gemini adversarial mathematical research orchestrator.

No third-party Python dependencies are required (Python 3.11+).

The agents are intentionally run read-only. This process writes only under
research_lab/rounds and research_lab/runtime.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import tomllib
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "research_lab"
CONFIG_PATH = LAB / "config.toml"
PROMPTS = LAB / "prompts"


class AgentRunError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("rb") as fh:
        return tomllib.load(fh)


def abs_path(rel: str) -> Path:
    return ROOT / rel


def executable(binary: str) -> str:
    found = shutil.which(binary)
    if not found:
        raise AgentRunError(f"Executable not found on PATH: {binary}")
    return found


def windows_wrap(argv: list[str]) -> list[str]:
    """Make .cmd/.bat launch reliable under subprocess on Windows."""
    if os.name != "nt" or not argv:
        return argv
    suffix = Path(argv[0]).suffix.lower()
    if suffix in {".cmd", ".bat"}:
        return ["cmd.exe", "/d", "/s", "/c", *argv]
    return argv


def run_process(
    argv: list[str],
    *,
    stdin_text: str | None,
    timeout: int,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    argv = windows_wrap(argv)
    try:
        return subprocess.run(
            argv,
            input=stdin_text,
            cwd=str(cwd),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AgentRunError(f"Timeout after {timeout}s: {' '.join(argv[:5])}") from exc


def render(template_name: str, **values: str) -> str:
    out = read_text(PROMPTS / template_name)
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def state_bundle(cfg: dict[str, Any]) -> str:
    paths = cfg["paths"]
    sections = [
        ("CURRENT CLAIM", abs_path(paths["claim"])),
        ("CERTIFIED FACTS", abs_path(paths["certified_facts"])),
        ("OPEN OBLIGATIONS", abs_path(paths["open_obligations"])),
        ("REJECTED ARGUMENTS", abs_path(paths["rejected_arguments"])),
    ]
    runtime = abs_path(paths["runtime_dir"]) / "WORKING_STATE.md"
    if runtime.exists():
        sections.append(("AUTOMATED WORKING STATE — NOT CERTIFIED", runtime))

    chunks: list[str] = []
    for title, path in sections:
        chunks.append(f"\n===== {title} =====\n{read_text(path)}")
    return "\n".join(chunks)


def run_codex(
    prompt: str,
    cfg: dict[str, Any],
    round_dir: Path,
    label: str,
    *,
    structured: bool = False,
) -> str | dict[str, Any]:
    ccfg = cfg["codex"]
    binary = executable(ccfg["binary"])
    final_path = round_dir / f"{label}.final.txt"
    events_path = round_dir / f"{label}.events.jsonl"
    stderr_path = round_dir / f"{label}.stderr.txt"

    argv = [
        binary,
        "exec",
        "--json",
        "--sandbox",
        ccfg["sandbox"],
        "--model",
        ccfg["model"],
        "-c",
        f'model_reasoning_effort="{ccfg["reasoning_effort"]}"',
        "-o",
        str(final_path),
    ]
    if structured:
        argv += ["--output-schema", str(abs_path(cfg["paths"]["schema"]))]
    argv += ["-"]

    proc = run_process(
        argv,
        stdin_text=prompt,
        timeout=int(ccfg["timeout_seconds"]),
    )
    write_text(events_path, proc.stdout)
    write_text(stderr_path, proc.stderr)

    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout)[-3000:]
        raise AgentRunError(f"Codex failed ({proc.returncode}): {tail}")

    if not final_path.exists():
        raise AgentRunError("Codex completed without --output-last-message file")

    final = read_text(final_path).strip()
    if not structured:
        write_text(round_dir / f"{label}.md", final + "\n")
        return final

    try:
        result = json.loads(final)
    except json.JSONDecodeError as exc:
        raise AgentRunError(f"Codex adjudicator returned invalid JSON: {final[:1200]}") from exc

    write_text(
        round_dir / "adjudication.json",
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
    )
    return result


def extract_gemini_response(raw: str) -> str:
    """Extract the response field from current Gemini CLI JSON, with fallbacks."""
    raw = raw.strip()
    if not raw:
        return ""

    candidates = [raw]
    first_brace = raw.find("{")
    if first_brace > 0:
        candidates.append(raw[first_brace:])

    obj: Any = None
    for candidate in candidates:
        try:
            obj = json.loads(candidate)
            break
        except json.JSONDecodeError:
            continue

    if obj is None:
        return raw

    if isinstance(obj, dict):
        for key in ("response", "text", "message", "content", "output"):
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    def collect_strings(node: Any, keys: set[str]) -> list[str]:
        found: list[str] = []
        if isinstance(node, dict):
            for key, value in node.items():
                if key in keys and isinstance(value, str) and value.strip():
                    found.append(value.strip())
                else:
                    found.extend(collect_strings(value, keys))
        elif isinstance(node, list):
            for item in node:
                found.extend(collect_strings(item, keys))
        return found

    strings = collect_strings(obj, {"response", "text", "content"})
    return max(strings, key=len) if strings else raw


def run_gemini(
    prompt: str,
    cfg: dict[str, Any],
    round_dir: Path,
    label: str,
) -> str:
    gcfg = cfg["gemini"]
    binary = executable(gcfg["binary"])
    raw_path = round_dir / f"{label}.raw.json"
    stderr_path = round_dir / f"{label}.stderr.txt"

    argv = [
        binary,
        "--approval-mode",
        gcfg["approval_mode"],
        "--output-format",
        gcfg["output_format"],
    ]
    if gcfg.get("model"):
        argv += ["--model", gcfg["model"]]

    # stdin carries the large research context, avoiding Windows command-line limits.
    argv += [
        "-p",
        (
            "READ-ONLY MATHEMATICAL RESEARCH. Read the full task from stdin. "
            "Never exit Plan Mode, never modify files, never run git writes. "
            "Return only your research report."
        ),
    ]

    proc = run_process(
        argv,
        stdin_text=prompt,
        timeout=int(gcfg["timeout_seconds"]),
    )
    write_text(raw_path, proc.stdout)
    write_text(stderr_path, proc.stderr)

    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout)[-3000:]
        raise AgentRunError(f"Gemini failed ({proc.returncode}): {tail}")

    response = extract_gemini_response(proc.stdout)
    if not response.strip():
        raise AgentRunError("Gemini completed with an empty response")
    write_text(round_dir / f"{label}.md", response + "\n")
    return response


def next_round_number(rounds_dir: Path) -> int:
    if not rounds_dir.exists():
        return 1
    nums: list[int] = []
    for child in rounds_dir.iterdir():
        if child.is_dir() and child.name.isdigit():
            nums.append(int(child.name))
    return max(nums, default=0) + 1


def working_state_markdown(round_no: int, verdict: dict[str, Any]) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None"

    return f"""# Automated working state — NOT CERTIFIED

Round: {round_no}

Status proposed by automated adjudicator: **{verdict['status']}**

## Rationale

{verdict['rationale']}

## Verified in this automated round

{bullets(verdict['verified_claims'])}

## Refuted in this automated round

{bullets(verdict['refuted_claims'])}

## Exact certificates reported

{bullets(verdict['exact_certificates'])}

## Computational evidence only

{bullets(verdict['computational_evidence'])}

## Surviving obligations

{bullets(verdict['surviving_obligations'])}

## Next target

{verdict['next_target']}

> This file is generated automatically. It does not amend CERTIFIED_FACTS.md.
"""


def obligation_signature(verdict: dict[str, Any]) -> str:
    payload = {
        "status": verdict.get("status"),
        "obligations": sorted(verdict.get("surviving_obligations", [])),
        "next_target": verdict.get("next_target", ""),
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def write_run_status(runtime_dir: Path, **data: Any) -> None:
    data["timestamp_epoch"] = time.time()
    write_text(
        runtime_dir / "RUN_STATUS.json",
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    )


def research_round(
    cfg: dict[str, Any],
    round_no: int,
    rounds_dir: Path,
) -> dict[str, Any]:
    round_dir = rounds_dir / f"{round_no:03d}"
    round_dir.mkdir(parents=True, exist_ok=True)

    state = state_bundle(cfg)
    write_text(round_dir / "state_snapshot.md", state)

    codex_prompt = render("codex_independent.md", STATE=state)
    gemini_prompt = render("gemini_independent.md", STATE=state)

    if cfg["lab"]["parallel_independent_pass"]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            c_future = pool.submit(
                run_codex, codex_prompt, cfg, round_dir, "codex_independent"
            )
            g_future = pool.submit(
                run_gemini, gemini_prompt, cfg, round_dir, "gemini_independent"
            )
            codex_independent = c_future.result()
            gemini_independent = g_future.result()
    else:
        codex_independent = run_codex(
            codex_prompt, cfg, round_dir, "codex_independent"
        )
        gemini_independent = run_gemini(
            gemini_prompt, cfg, round_dir, "gemini_independent"
        )

    codex_cross_prompt = render(
        "codex_cross_review.md",
        STATE=state,
        SELF_REPORT=str(codex_independent),
        PEER_REPORT=str(gemini_independent),
    )
    gemini_cross_prompt = render(
        "gemini_cross_review.md",
        STATE=state,
        SELF_REPORT=str(gemini_independent),
        PEER_REPORT=str(codex_independent),
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        c_future = pool.submit(
            run_codex, codex_cross_prompt, cfg, round_dir, "codex_cross_review"
        )
        g_future = pool.submit(
            run_gemini, gemini_cross_prompt, cfg, round_dir, "gemini_cross_review"
        )
        codex_cross = c_future.result()
        gemini_cross = g_future.result()

    adjudicator_prompt = render(
        "codex_adjudicator.md",
        STATE=state,
        CODEX_INDEPENDENT=str(codex_independent),
        GEMINI_INDEPENDENT=str(gemini_independent),
        CODEX_CROSS=str(codex_cross),
        GEMINI_CROSS=str(gemini_cross),
    )
    verdict = run_codex(
        adjudicator_prompt,
        cfg,
        round_dir,
        "codex_adjudicator",
        structured=True,
    )
    assert isinstance(verdict, dict)
    return verdict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=None,
        help="Override config.toml max_rounds for this run.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run exactly one research round.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate files/executables and print the current state without calling agents.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cfg = load_config()

    rounds_dir = abs_path(cfg["paths"]["rounds_dir"])
    runtime_dir = abs_path(cfg["paths"]["runtime_dir"])
    rounds_dir.mkdir(parents=True, exist_ok=True)
    runtime_dir.mkdir(parents=True, exist_ok=True)

    # Fail early before a long unattended run.
    executable(cfg["codex"]["binary"])
    executable(cfg["gemini"]["binary"])

    if args.dry_run:
        print(state_bundle(cfg))
        print("\nDRY RUN OK: Codex and Gemini executables are available.")
        return 0

    configured_max = int(cfg["lab"]["max_rounds"])
    max_rounds = 1 if args.once else (args.max_rounds or configured_max)
    proof_needed = int(cfg["lab"]["proof_confirmation_rounds"])
    max_stale = int(cfg["lab"]["max_stale_rounds"])

    proof_streak = 0
    stale_streak = 0
    previous_signature: str | None = None

    write_run_status(runtime_dir, status="RUNNING", max_rounds=max_rounds)

    for _ in range(max_rounds):
        round_no = next_round_number(rounds_dir)
        print(f"\n=== Research round {round_no:03d} ===", flush=True)

        try:
            verdict = research_round(cfg, round_no, rounds_dir)
        except AgentRunError as exc:
            write_run_status(
                runtime_dir,
                status="AGENT_ERROR_OR_QUOTA",
                round=round_no,
                error=str(exc),
            )
            print(f"STOP: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:  # Keep unattended runs diagnosable.
            write_run_status(
                runtime_dir,
                status="UNEXPECTED_ERROR",
                round=round_no,
                error=repr(exc),
            )
            raise

        write_text(
            runtime_dir / "LATEST_VERDICT.json",
            json.dumps(verdict, ensure_ascii=False, indent=2) + "\n",
        )
        write_text(
            runtime_dir / "WORKING_STATE.md",
            working_state_markdown(round_no, verdict),
        )

        status = verdict["status"]
        obligations = verdict["surviving_obligations"]
        print(f"Status: {status}")
        print(f"Surviving obligations: {len(obligations)}")
        print(f"Next: {verdict['next_target']}")

        signature = obligation_signature(verdict)
        if signature == previous_signature:
            stale_streak += 1
        else:
            stale_streak = 0
        previous_signature = signature

        if status == "PROVED" and not obligations:
            proof_streak += 1
        else:
            proof_streak = 0

        exact_refutation = (
            status == "REFUTED"
            and bool(verdict["exact_certificates"])
            and bool(cfg["lab"]["stop_on_exact_refutation"])
        )
        if exact_refutation:
            write_run_status(
                runtime_dir,
                status="STOP_EXACT_REFUTATION_FOR_HUMAN_REVIEW",
                round=round_no,
            )
            print("STOP: exact refutation candidate; human review required.")
            return 0

        if proof_streak >= proof_needed:
            write_run_status(
                runtime_dir,
                status="STOP_PROOF_CANDIDATE_FOR_HUMAN_REVIEW",
                round=round_no,
                proof_confirmation_rounds=proof_streak,
            )
            print("STOP: repeated proof candidate with no obligations; human review required.")
            return 0

        if verdict.get("stop_recommendation") and status not in {"OPEN", "CONDITIONAL"}:
            write_run_status(
                runtime_dir,
                status="STOP_AGENT_RECOMMENDATION_FOR_HUMAN_REVIEW",
                round=round_no,
            )
            print("STOP: adjudicator recommends human review.")
            return 0

        if stale_streak >= max_stale:
            write_run_status(
                runtime_dir,
                status="STOP_STALEMATE",
                round=round_no,
                stale_rounds=stale_streak,
            )
            print("STOP: obligations stopped changing.")
            return 0

    write_run_status(runtime_dir, status="STOP_MAX_ROUNDS")
    print("STOP: maximum rounds reached.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
