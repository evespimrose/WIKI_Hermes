#!/usr/bin/env python3
"""Resolve the LLM Wiki repo's raw/ folder ON THIS MACHINE.

The wiki is ONE git repo synced across many machines through a shared remote,
so its absolute path is different on every machine. We therefore NEVER hardcode
the path. We identify the repo by its canonical git *remote* and then use the
`raw/` folder *relative* to whatever root that repo happens to live at locally.

Resolution order (first hit wins, every hit is validated by the remote):
  1. --root <path>      explicit override (validated + cached)
  2. cache file         `.wiki_root_cache` next to this script
  3. $WIKI_REPO_ROOT    environment variable
  4. probe candidates   cwd ancestors, ~, drive hints — each VALIDATED by remote

Prints the absolute `<repo_root>/raw` path (created if missing) to stdout.
Exits 1 (with guidance) if the wiki clone cannot be found.
"""
import os
import re
import sys
import subprocess
import pathlib

# Canonical cross-machine identity of the wiki. owner/repo, lowercased.
# Matches https + ssh forms, with or without a trailing ".git".
CANONICAL = "evespimrose/wiki"
CACHE = pathlib.Path(__file__).with_name(".wiki_root_cache")


def repo_id(url: str) -> str:
    """Reduce any GitHub remote URL to 'owner/repo' (lowercased)."""
    if not url:
        return ""
    m = re.search(r"github\.com[/:]+([^/]+)/([^/]+?)(?:\.git)?/?$", url.strip(), re.I)
    return f"{m.group(1).lower()}/{m.group(2).lower()}" if m else ""


def _git(d: pathlib.Path, *args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(d), *args],
            capture_output=True, text=True, timeout=8,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def wiki_root(d) -> pathlib.Path | None:
    """Return the repo top-level if `d` is inside the canonical wiki, else None."""
    if not d:
        return None
    d = pathlib.Path(d).expanduser()
    if not d.is_dir():
        return None
    top = _git(d, "rev-parse", "--show-toplevel")
    if not top:
        return None
    root = pathlib.Path(top)
    if repo_id(_git(root, "remote", "get-url", "origin")) == CANONICAL:
        return root
    return None


def candidates():
    """Ordered, de-duplicated probe list. Nothing here is trusted blindly —
    each is validated by wiki_root() before use."""
    seen = []

    def add(p):
        if not p:
            return
        p = pathlib.Path(p).expanduser()
        if p not in seen:
            seen.append(p)

    add(os.environ.get("WIKI_REPO_ROOT"))

    cwd = pathlib.Path.cwd()
    for anc in [cwd, *cwd.parents]:
        add(anc)
        add(anc / "WIKI")
        add(anc / "wiki")

    home = pathlib.Path.home()
    for name in ("WIKI", "wiki", "Unity/WIKI", "Documents/WIKI", "repos/WIKI"):
        add(home / name)

    if os.name == "nt":
        drive = pathlib.Path(cwd.anchor)  # e.g. "D:\\"
        for sub in ("Unity/WIKI", "WIKI"):
            add(drive / sub)
        for dl in "CDEFG":
            add(pathlib.Path(f"{dl}:/Unity/WIKI"))
            add(pathlib.Path(f"{dl}:/WIKI"))

    return seen


def main():
    args = sys.argv[1:]
    explicit = args[args.index("--root") + 1] if "--root" in args else None

    root = None
    if explicit:
        root = wiki_root(explicit)
        if not root:
            sys.exit(
                f"ERROR: --root '{explicit}' is not the wiki clone "
                f"(its origin != {CANONICAL})."
            )

    if not root and CACHE.exists():
        root = wiki_root(CACHE.read_text(encoding="utf-8").strip())

    if not root:
        for c in candidates():
            root = wiki_root(c)
            if root:
                break

    if not root:
        sys.exit(
            "ERROR: the wiki clone (github.com/" + CANONICAL + ") was not found "
            "on this machine.\n"
            "Fix: set env WIKI_REPO_ROOT=<path to your local WIKI clone>, "
            "or re-run with --root <path>."
        )

    CACHE.write_text(str(root), encoding="utf-8")
    # --subdir <rel> resolves any repo-relative folder (created if missing).
    # Default "raw" keeps backward compatibility; distill also needs docs/analysis.
    sub = args[args.index("--subdir") + 1] if "--subdir" in args else "raw"
    target = root.joinpath(*[p for p in sub.replace("\\", "/").split("/") if p])
    target.mkdir(parents=True, exist_ok=True)
    print(str(target))


if __name__ == "__main__":
    main()
