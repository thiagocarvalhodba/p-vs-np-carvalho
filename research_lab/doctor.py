#!/usr/bin/env python3
"""Environment checks for the Codex × Gemini research lab."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "research_lab" / "config.toml"


def command(binary: str, *args: str) -> list[str]:
    found = shutil.which(binary)
    if not found:
        raise FileNotFoundError(binary)
    argv = [found, *args]
    if os.name == "nt" and Path(found).suffix.lower() in {".cmd", ".bat"}:
        argv = ["cmd.exe", "/d", "/s", "/c", *argv]
    return argv


def check(binary: str) -> bool:
    try:
        proc = subprocess.run(
            command(binary, "--version"),
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
    except FileNotFoundError:
        print(f"[FAIL] {binary}: not found on PATH")
        return False
    except Exception as exc:
        print(f"[FAIL] {binary}: {exc}")
        return False

    first = (proc.stdout or "").strip().splitlines()
    version = first[0] if first else f"exit={proc.returncode}"
    mark = "OK" if proc.returncode == 0 else "FAIL"
    print(f"[{mark}] {binary}: {version}")
    return proc.returncode == 0


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 11):
        print("[FAIL] Python 3.11+ required (tomllib).")
        return 2

    with CFG.open("rb") as fh:
        cfg = tomllib.load(fh)

    ok = True
    ok &= check(cfg["codex"]["binary"])
    ok &= check(cfg["gemini"]["binary"])

    required = [
        cfg["paths"]["claim"],
        cfg["paths"]["certified_facts"],
        cfg["paths"]["open_obligations"],
        cfg["paths"]["rejected_arguments"],
        cfg["paths"]["schema"],
    ]
    for rel in required:
        path = ROOT / rel
        exists = path.exists()
        print(f"[{'OK' if exists else 'FAIL'}] {rel}")
        ok &= exists

    print("\nSafety defaults:")
    print(f"  Codex sandbox: {cfg['codex']['sandbox']}")
    print(f"  Gemini approval mode: {cfg['gemini']['approval_mode']}")
    print("  Automatic git push/merge: disabled")

    if ok:
        print("\nEnvironment looks ready. Run: .\\research_lab\\run.ps1")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
