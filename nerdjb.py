#!/usr/bin/env python3
"""nerdjb: legal-by-design wrapper for an existing Xbox GE-Proton setup.

No personal paths, game files, keys, firmware, DRM tools or proprietary
binaries are embedded. All locations come from config.env or the environment.
No frame generation, resolution changes or graphics-setting changes are applied.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.env"

REPO: Path
GAME: Path
RUNTIME: Path
PROTON: Path
PRESET: Path
L: Any

# The proven stable shape only. No tuned/unvalidated flags.
BASE = {
    "VICTORY_FSR_4K": "performance",
    "VICTORY_PORT_CBV": "1",
    "VICTORY_PORT_GUARD": "1",
    "VICTORY_PORT_JOURNAL": "1",
    "VICTORY_KBM_GTA": "1",
    "VICTORY_D3D12_DRED": "0",
    "VICTORY_THIN": "0",
    "VICTORY_JOIN_PARTS": "0",
    "VICTORY_UPLOAD_AHEAD": "0",
    "VICTORY_PORT_CONSTANTS": "1",
    "VICTORY_PORT_DESCRIPTORS": "1",
    "VICTORY_COPY_COMPARE": "1",
    "VICTORY_ONE_PAD": "0",
    "VICTORY_FRAME_INTERVAL_MS": "0",
    "VICTORY_SKIP_PIPELINES": "none",
}

FORBIDDEN_SUFFIXES = {".zar", ".exe", ".dll", ".bin", ".elf", ".pkg", ".rap", ".pdb"}
FORBIDDEN_NAMES = {"eboot.bin", "game_scarlett_master.exe"}
FORBIDDEN_PARTS = ("key", "firmware", "decrypt", "jailbreak", "bypass_drm")
PLACEHOLDER_MARKERS = ("path/to", "your-", "placeholder", "<")


def load_config() -> None:
    """Read only path settings from config.env; never add dumps or secrets there."""
    if not CONFIG.is_file():
        return
    for raw in CONFIG.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("VICTORY_NERDJB_") or key == "VICTORY_PROTON_PREFIX":
            os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def env_path(name: str) -> Path:
    value = os.environ.get(name, "").strip()
    lowered = value.lower()
    if not value or any(marker in lowered for marker in PLACEHOLDER_MARKERS):
        raise RuntimeError(f"Set {name} to a real path in config.env before running nerdjb.")
    return Path(value).expanduser().resolve()


def resolve_paths() -> None:
    global REPO, GAME, RUNTIME, PROTON, PRESET, L
    REPO = env_path("VICTORY_NERDJB_REPO")
    GAME = env_path("VICTORY_NERDJB_GAME")
    RUNTIME = env_path("VICTORY_NERDJB_RUNTIME")
    PROTON = env_path("VICTORY_NERDJB_PROTON")
    PRESET = REPO / "scripts" / "windows-preset.json"
    scripts = str(REPO / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import launcher as launcher_module

    L = launcher_module


def legal_check() -> None:
    skip_dirs = {".git", "__pycache__", "logs", "_Build", ".venv", "venv"}
    bad: list[str] = []
    for path in HERE.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.relative_to(HERE).parts):
            continue
        name = path.name.lower()
        stem = path.stem.lower()
        if (
            path.suffix.lower() in FORBIDDEN_SUFFIXES
            or name in FORBIDDEN_NAMES
            or any(part in stem for part in FORBIDDEN_PARTS)
        ):
            bad.append(str(path.relative_to(HERE)))
    for key, value in os.environ.items():
        upper = key.upper()
        if any(token in upper for token in ("FRAMEGEN", "FRAME_GEN", "FIDELITYFX_FRAMEGEN")) and value not in (
            "",
            "0",
        ):
            bad.append(f"env:{key}")
    if bad:
        raise RuntimeError("nerdjb legal check failed; forbidden material/toggle found:\n  " + "\n  ".join(bad))
    print("legal_check=ok", flush=True)


def paths_check() -> None:
    for label, path in (("repo", REPO), ("game", GAME), ("runtime", RUNTIME), ("proton", PROTON), ("preset", PRESET)):
        if not path.exists():
            raise FileNotFoundError(f"{label}: {path}")
    print("paths_check=ok", flush=True)


def env_for() -> dict[str, str]:
    preset = json.loads(PRESET.read_text(encoding="utf-8"))
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("VICTORY_") or k in preset["keep"]}
    env.update(preset["base"])
    env.update(preset["fast"])
    env.update(BASE)
    env["MESA_SHADER_CACHE_MAX_SIZE"] = "16G"

    config = REPO / "victory.toml"
    if config.is_file() and "VICTORY_CONFIG" not in env:
        env["VICTORY_CONFIG"] = L.windows_path(config)
    for key in (
        "VICTORY_CONFIG",
        "VICTORY_GAME_DIR",
        "VICTORY_CACHE_DIR",
        "VICTORY_DATA_DIR",
        "VICTORY_FIDELITYFX_DIR",
    ):
        value = env.get(key, "")
        if value.startswith("/"):
            env[key] = L.windows_path(value)

    prefix = L.proton_prefix()
    prefix.mkdir(parents=True, exist_ok=True)
    info = L.prepare_proton_prefix(PROTON, prefix, env)
    dxc = L.dxc_source(env)
    if dxc is not None:
        dxil, _ = dxc
        in_prefix = prefix / "pfx" / "drive_c" / "windows" / "system32" / "dxil.dll"
        chosen = in_prefix if in_prefix.is_file() else dxil
        env["VICTORY_DXIL"] = L.windows_path(chosen)
        dxc_exe = chosen.parent / "dxc.exe"
        if not dxc_exe.is_file():
            dxc_exe = dxil.parent / "dxc.exe"
        if dxc_exe.is_file():
            env["VICTORY_PC_DXC"] = L.windows_path(dxc_exe)

    steam_roots = L.steam_roots()
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(steam_roots[0] if steam_roots else Path.home() / ".steam/steam")
    env["STEAM_COMPAT_DATA_PATH"] = str(prefix)
    env.setdefault("SteamGameId", "0")
    env.setdefault("SteamAppId", "0")
    env.setdefault("PROTONFIXES_DISABLE", "1")
    print("dll_info=", info, flush=True)
    print("overrides=", env.get("WINEDLLOVERRIDES", ""), flush=True)
    return env


def do_warm() -> int:
    env = env_for()
    command = [
        str(PROTON),
        "runinprefix",
        L.windows_path(RUNTIME),
        "warm",
        "--used",
        "--again",
        "--jobs",
        "8",
    ]
    log = L.data_root() / "logs" / "nerdjb-warm.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    print("warm_log=", log, flush=True)
    with log.open("wb") as out:
        out.write((" ".join(command) + "\n").encode())
        out.flush()
        return subprocess.run(
            command,
            cwd=GAME.parent,
            env=env,
            stdout=out,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            check=False,
        ).returncode


def do_run() -> int:
    log = L.data_root() / "logs" / "nerdjb-run.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    if log.exists():
        log.unlink()
    session = L.Launch(
        game=GAME,
        log=log,
        console="series-x",
        build="diag",
        fps=0,
        safe=False,
        ray_tracing=False,
        rebuild=False,
        overrides=dict(BASE),
        runtime=RUNTIME,
        proton=PROTON,
        preset=PRESET,
    )
    print("profile=stable", flush=True)
    print("runtime=", RUNTIME, flush=True)
    print("proton=", PROTON, flush=True)
    print("log=", log, flush=True)
    print("flags=", json.dumps(BASE, sort_keys=True), flush=True)
    return L.run_linux(session)


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("check", "warm", "run"))
    args = cli.parse_args()
    try:
        load_config()
        legal_check()
        resolve_paths()
        paths_check()
        if args.action == "check":
            return 0
        if args.action == "warm":
            return do_warm()
        return do_run()
    except (ImportError, OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"nerdjb: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
