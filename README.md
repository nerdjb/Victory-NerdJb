# nerdjb

Local-only, legal-by-design label for a **thin wrapper** around an existing Xbox
GE-Proton setup. This is **not** a new emulator, not a game fork, and not a
compatibility claim. It contains only text files written here.

## What it is

- A small Python wrapper that calls components you already installed:
  - GE-Proton 11-14 with the already-patched `wineserver`
  - your existing `victory.exe` build
  - your existing Proton prefix, save, cache and FidelityFX paths
- A shader-warm entry point that reuses the native-D3D12 warm path.
- A stability check that refuses to run if forbidden material or framegen
  toggles are present.

No personal paths, folder names, game files or binaries are embedded. Paths come
from `config.env`, which is ignored by Git and never published.

## Docs

- [Linux setup](SETUP-LINUX.md)
- [Windows setup](SETUP-WINDOWS.md)
- [Publish checklist](PUBLISH.md)
- [Legal notice](NOTICE.md)

## Legal boundary

This project:

- does not jailbreak any console;
- does not extract, derive, share or use encryption keys;
- does not decrypt, unpack, bypass or defeat DRM;
- does not include game dumps, packages, saves, firmware, system images or keys;
- does not include Microsoft/Sony/console DLLs, SDK binaries or proprietary blobs;
- makes no network calls and has no updater or telemetry.

You supply your own legally obtained dump and any system components in your own
prefix. Whether your use is lawful depends on your jurisdiction and agreements;
this is not legal advice.

## Strict runtime rules

- GE-Proton only on the Linux/Proton path.
- No frame generation of any kind.
- No output or internal resolution changes.
- No in-game graphics-setting changes.
- Same save, cache and FidelityFX paths as the existing launcher.
- No `THIN`, `JOIN_PARTS`, `UPLOAD_AHEAD`, or PR #477 copy-back changes.
- No `CARD_BUFFERS_MIN_KB=64`; the best measured run used the default grid `4096`.

## Quick start

```bash
cp config.example.env config.env
# edit config.env with your own paths; never add dumps, keys or secrets
python3 nerdjb.py check
python3 nerdjb.py warm
python3 nerdjb.py run
```

`nerdjb` is a local name only. No remote is configured and nothing is published.
