#!/usr/bin/env python3
"""Package integrity check: compare the user's own copy against a published hash manifest.

Usage: verify_package.py --game-dir <dir> [--manifest <json|url>]
Default manifest: Leonida's public per-file size+SHA256 manifest (hashes only, no content).
Prints per-file PASS/FAIL/MISSING; exit 0 iff all listed files pass.
"""
import argparse, hashlib, json, os, sys, urllib.request

DEFAULT_MANIFEST = ("https://raw.githubusercontent.com/ItsNotRexed/Leonida/main/"
                    "game/xbox-1.0.2.1.json")

def load_manifest(src):
    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=30) as r:
            return json.loads(r.read())
    return json.load(open(src))

def sha256(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game-dir", required=True)
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    a = ap.parse_args()
    man = load_manifest(a.manifest)
    files = man.get("files") or {}
    ok = bad = missing = 0
    for name, meta in files.items():
        p = os.path.join(a.game_dir, name)
        if not os.path.exists(p):
            print(f"MISSING {name}")
            missing += 1
            continue
        h = sha256(p)
        if h == meta.get("sha256"):
            ok += 1
        else:
            print(f"FAIL    {name} sha={h}")
            bad += 1
    print(f"== package: {ok} pass, {bad} fail, {missing} missing ==")
    if missing:
        print("note: a missing required archive can flip the title into an early assert "
              "(see docs/known-signatures.md)")
    sys.exit(0 if bad == 0 and missing == 0 else 1)

if __name__ == "__main__":
    main()
