# Windows setup (native Windows path)

`nerdjb.py` wraps GE-Proton, so it does **not** run natively on Windows. This doc
covers the native Windows side of the same **stable profile**. It is still a
legal-by-design setup: no game files, keys, firmware, DRM tools, DLLs or personal
paths are bundled here.

## What you supply

- Windows 10/11 x64 and a D3D12 GPU with SM 6.6 + mesh shaders.
- Your existing VIctory Windows launcher/build scripts (not included here).
- A legally obtained, unpacked Xbox Series X|S title folder. Keep it outside this
  wrapper folder.
- Any DXC/D3D12/Agility components you already installed yourself. `nerdjb`
  never vendors them.

Nothing here jailbreaks a console, extracts keys, decrypts packages or bypasses
DRM. This is not legal advice.

## Steps

1. Open your existing VIctory Windows launcher.
2. Add your title by pointing it at your own unpacked folder. Do **not** copy the
   game into this wrapper.
3. Select:
   - console: `series-x`
   - build: the build name of your existing stable binary
   - FPS limit: `0`
   - Safe mode: off
   - Ray tracing: off
   - Rebuild: off
4. In **Advanced → Environment overrides**, paste the stable block below.
5. Launch normally. Logs stay in your own local application-data directory, not
   in this wrapper.

## Stable override block

```text
VICTORY_FSR_4K=performance
VICTORY_PORT_CBV=1
VICTORY_PORT_GUARD=1
VICTORY_PORT_JOURNAL=1
VICTORY_KBM_GTA=1
VICTORY_D3D12_DRED=0
VICTORY_THIN=0
VICTORY_JOIN_PARTS=0
VICTORY_UPLOAD_AHEAD=0
VICTORY_PORT_CONSTANTS=1
VICTORY_PORT_DESCRIPTORS=1
VICTORY_COPY_COMPARE=1
VICTORY_ONE_PAD=0
VICTORY_FRAME_INTERVAL_MS=0
VICTORY_SKIP_PIPELINES=none
```

Do not add any framegen toggle, resolution override, graphics preset,
`CARD_BUFFERS_MIN_KB=64`, or copy-back patch. FSR4K stays launcher-managed.

## Privacy before sharing

Never commit `config.env`, logs, saves or your game path. See
[PUBLISH.md](PUBLISH.md) for the privacy check; it should print no files.

## Known limits

- No frame generation.
- No output/internal resolution change.
- No in-game graphics-setting change.
- No proven 30 fps; this profile favors stability and the same save/paths.
- The Windows path is separate from the tested Linux/GE-Proton wrapper.
