# Hardware coverage matrix (community reports)

Every row is a reported observation; **Self** = produced with this bench, others link upstream.
"A black frame" is not a picture; a milestone counts only with the evidence named.

| GPU (class) | Driver | Layer | Furthest milestone | Evidence | Source |
|---|---|---|---|---|---|
| RX 9070 (RDNA4) | – | xcl main | menu @30 fps | owner statement, 548 tests | xcl #195 |
| RX 7800 XT (RDNA3) | – | xcl + #203+#215 stack | title screen + Navigation menu (quads one-triangle defect) | screenshots in PR | xcl #203 |
| RX 6700 XT (RDNA2) | – | VICTORY | menus 30 fps, intro w/ sound; world black | single-machine | VIctory README |
| RTX 3060 (Ampere) | – | xcl + #203+#187 | whole first-boot flow | comment | xcl #203 thread |
| RTX 2070 Super (Turing) | – | xcl | menus, then `+0x13936` crash | log excerpt | xcl #298 |
| RTX 5070 Ti (Blackwell) | 616.92 | xcl main `d4f17ca` | menu, 3,599 presents/270 s @15–28 fps | full report | xcl #232 comment |
| RTX 3080 (Ampere) | – | xcl `af20b4b` | PLAYER1 account screen; later `+0x3e42541` | committed png | nvdw1/gta6-first-frame-on-pc |
| RTX 3080 Ti (Ampere) | 32.0.16.2124 | xcl main / +#267 / +#203+#187 | **no presents**; early assert tied to a missing archive | Self runs | xcl #301; VIctory #8 |
| RTX 3080 Ti (Ampere) | 32.0.16.2124 | VICTORY `e8f3b1c` | crash moved `+0x2237178` → `+0x1ce6e13` once `appdata0.rpf` present | Self runs | this repo |

## How to add a row

Run `harness/run_dut.ps1`, then `checkers/scoreboard.py`; post the scoreboard output and the
signature (RVA) in a PR to this file plus the relevant upstream issue. No game data, no logs
quoting payloads.
