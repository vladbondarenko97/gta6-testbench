# Known crash signatures (cross-layer)

Match by **RVA + register fingerprint**, because different conditions can share an exception code.
All entries are evidence-linked to an upstream report; none contain game data.

| Signature | Trigger/meaning | Evidence |
|---|---|---|
| `0x80000003 @ title+0x2237178`, regs `rax=0 rbx=0 rcx=0 rdx=0x66 r8=0x7efefefefefefeff r9=0x7f656f712d2f6073`, 0 presents | seen when a **required top-level archive is absent** (`appdata0.rpf`); reproduced independently in VICTORY by omitting it, resolved when restored | VIctory PR #12, VIctory issue #8, xcl issue #301 |
| `0x80000003 @ title+0x1ce6e13` | next assert after `appdata0.rpf` present; currently open in our bench | this repo's run log |
| `0xc0000005 write @ title+0x2215c35` after stalled frames | title hang watchdog (decoded upstream: `Sleep(1000)` slot threshold → null write → `int3`) | xcl #232, #156 |
| `0xc0000005 write @ title+0x13936` | reported after menus on RTX 2070 Super | xcl #298 |
| `0x80000003 @ title+0x3e42541` | reported after PLAYER1 account screen (RTX 3080) | nvdw1/gta6-first-frame-on-pc |

## Register fingerprints

The `r8/r9` pair above is stable across hosts for the missing-archive condition
(`0x7efefefefefefeff` / `0x7f656f712d2f6073`), which makes it useful for correlating reports
across layers without shipping dumps.
