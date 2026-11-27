# Linux setup (CachyOS/Arch-style)

`nerdjb` is a **wrapper** around components you already have. It does not include
a game, firmware, keys, DRM tools or proprietary DLLs. No personal paths are
embedded in the published files.

## Requirements you supply

- GE-Proton 11-14 with the already-patched `wineserver`.
- Your own `victory.exe` build.
- Your existing Proton prefix, save directory, cache and FidelityFX directory.
- A legally obtained, unpacked Xbox Series X|S game directory/exe.
- RADV/Vulkan 1.3-capable AMD GPU and current Mesa driver.
- Any Windows DLLs you already placed in your own prefix. `nerdjb` never bundles them.

## Steps

```bash
cd /path/to/nerdjb
cp config.example.env config.env
# edit config.env with your own paths; never add dumps, keys or secrets

python3 nerdjb.py check
python3 nerdjb.py warm
python3 nerdjb.py run
```

`config.env` is loaded automatically; you do not need to `source` it.

- `check` inspects the wrapper folder and verifies that configured paths exist.
- `warm` compiles host pipelines with the same native-D3D12 prefix setup as a real launch.
- `run` starts the title with the proven stable flags.

## What is intentionally fixed

- No frame generation.
- No output/internal resolution change.
- No in-game graphics-setting change.
- No `THIN`, `JOIN_PARTS`, `UPLOAD_AHEAD`, or PR #477 copy-back path.
- No `CARD_BUFFERS_MIN_KB=64`; the best measured run used the default `4096`.
- Same save/cache/FidelityFX paths as the existing launcher.

## Logs

Logs stay in your own data directory, not in the published wrapper:

- warm: `$XDG_DATA_HOME/victory-rdna/logs/nerdjb-warm.log`
- run: `$XDG_DATA_HOME/victory-rdna/logs/nerdjb-run.log`

## Privacy before publishing

See [PUBLISH.md](PUBLISH.md) for the privacy check. It should print no files.

## Legal

Only use dumps you lawfully obtained. `nerdjb` does not jailbreak, decrypt,
extract keys, bypass DRM or include protected material. This is not legal advice.
