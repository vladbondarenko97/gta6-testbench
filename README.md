# gta6-testbench

A **DUT-agnostic conformance and regression testbench** for community GTA VI PC port layers.

Each compatibility layer (XCL, VICTORY, PercyScarlett, …) is treated as a device under test:
the harness applies a standard stimulus (launch against the user's own copy), observes the
output (logs, `report.json`, frame dumps, crash signatures), and the scoreboard compares it
against expected milestones. Coverage tracks which hardware/driver combinations actually pass.

```
harness/    launch a DUT with isolation, logging and frame capture
checkers/   scoreboard: milestones, crash-signature fingerprints, frame analysis
verify/     package integrity check against published per-file hashes
privacy/    guest network isolation (firewall) for DUT processes
docs/       known-signature index, hardware coverage matrix, upstream links
```

## Content policy (strict)

- **No game data.** No archives, executables, extracted assets, names lists or payloads.
- **No keys or key material.** This repo never contains or references any.
- Users bring their own copy; scripts only read it.
- Reports contain hashes, counts, register/stack fingerprints and log lines that the layer
  itself printed — never file contents.

## Quick start

```powershell
# 1. verify your own copy (hashes only)
python verify/verify_package.py --game-dir D:\GTA6\GTA6.Xbox.v1.0.2.1

# 2. isolate the DUT from the network (recommended before any run)
powershell -File privacy/block_guest_network.ps1 -Exe "C:\xcl\target\release\xcl.exe"

# 3. run a DUT and score it
powershell -File harness/run_dut.ps1 -Dut xcl -Exe "C:\xcl\target\release\xcl.exe" -GameDir D:\GTA6\GTA6.Xbox.v1.0.2.1
python checkers/scoreboard.py --logs "$env:LOCALAPPDATA\XCL\<TitleId>\logs"
python checkers/analyze_frames.py "$env:LOCALAPPDATA\XCL\<TitleId>\logs"
```

## Status model

Milestones scored per run (same ladder the community tracker uses):

| Milestone | Evidence required |
|---|---|
| Loads | imports bound with `missing=0` (all package DLLs present), title enters its own code |
| Init survives | no first-chance exception before first present |
| Presents | `presents > 0` |
| Picture | non-black frame in a dump (analyzer output) |
| Menu | picture with menu-like content reachable (screenshot evidence) |

Crash signatures are matched by **RVA + register fingerprint**, not just the exception code,
so different layers' reports can be correlated. See `docs/known-signatures.md`.

## Known upstreams

This bench reports findings to the layers themselves:

- XCL — https://github.com/ivall/xcl
- VICTORY — https://github.com/Marvisak/VIctory
- PercyScarlett — https://github.com/rpatty-dev/PercyScarlett

MIT licensed. Not affiliated with any game publisher; no warranty.
