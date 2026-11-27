# Publish checklist ("upload it")

Nothing has been published. There is no configured remote and no commit, push or
pull request has been made by the assistant.

## Before upload

Run these from the wrapper folder:

```bash
python3 nerdjb.py check

# Should print no files. Excludes this checklist because it contains the patterns.
grep -RInE '(/home/|/mnt/|[A-Za-z]:\\Users\\)' --exclude=PUBLISH.md . || true

git status --short
```

Check that **none** of these are present or staged:

- game dumps, packages, `.zar`, `.pkg`, `.rap`, ELF/PE game executables;
- saves, firmware, system images, keys, decrypted files;
- Microsoft/Sony/console DLLs, SDK blobs, DXC/D3D12 binaries;
- `config.env`, logs, cache directories, build output;
- personal folder names or absolute paths in any published file.

The published files are only:

```text
.gitignore
LICENSE
NOTICE.md
PUBLISH.md
README.md
SETUP-LINUX.md
SETUP-WINDOWS.md
config.example.env
nerdjb.py
```

## Repo naming and description

Use the generic name `nerdjb`. Do not put a game title, console brand, "PC dump",
"crack", "key" or "30 fps" in the repo name, description or tags. Keep the
description to something like:

> Legal-by-design wrapper docs for an existing GE-Proton setup. No game files,
> keys, firmware or binaries included.

## Local git, only if you approve

```bash
git init
git add .gitignore LICENSE NOTICE.md PUBLISH.md README.md \
        SETUP-LINUX.md SETUP-WINDOWS.md config.example.env nerdjb.py
git status --short
git commit -m "Add legal-by-design nerdjb wrapper docs"

# Only after you supply a remote and explicitly approve publishing:
git remote add origin <your-remote-url>
git push -u origin main
```

## Current status

- Local folder only.
- No remote configured.
- No commit, push or PR made.
- If you want an upload, send the remote URL and confirm explicitly; placeholders
  stay in place and no personal paths are added.
