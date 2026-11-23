#!/usr/bin/env python3
"""Scoreboard: read a DUT's logs and emit milestone status + crash fingerprint.

Usage: scoreboard.py --logs <logs-dir> [--dut xcl|victory]
Handles xcl's report.json when present; falls back to log scanning for other layers.
No game data is read; only the layer's own log/report files.
"""
import argparse, json, os, re, sys

MILESTONES = ["loads", "init_survives", "presents", "picture", "menu"]

def score_xcl(logs):
    out = {}
    rp = os.path.join(logs, "report.json")
    if not os.path.exists(rp):
        return None, "no report.json"
    r = json.load(open(rp))
    d = r.get("d3d12", {})
    s = r.get("shaders", {})
    out["imports_missing"] = None
    out["presents"] = d.get("presents", 0)
    out["shaders_unique"] = s.get("unique", 0)
    out["translated_pipelines"] = d.get("translated_pipelines", 0)
    out["crash"] = (r.get("crash") or "")[:400]
    out["exit_code"] = r.get("exit_code")
    return out, rp

def score_log(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    res = {}
    for m in re.finditer(r"first-chance exception (0x[0-9a-fA-F]+) at [^+]*\+0x([0-9a-fA-F]+)(.*)", t):
        res["first_chance"] = {"code": m.group(1), "rva": "0x" + m.group(2), "regs": m.group(3).strip()[:300]}
        break
    bound = re.findall(r"bound\s+(\S+): (\d+) hle, (\d+) host, (\d+) title, (\d+) missing", t)
    res["imports"] = [{"module": b[0], "missing": int(b[4])} for b in bound]
    res["imports_all_bound"] = all(i["missing"] == 0 for i in res["imports"]) if bound else None
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", required=True)
    ap.add_argument("--dut", default=None)
    a = ap.parse_args()
    report, src = (score_xcl(a.logs) if (a.dut in (None, "xcl")) else (None, None))
    logres = None
    xl = os.path.join(a.logs, "xcl.log")
    if os.path.exists(xl):
        logres = score_log(xl)
    print("== scoreboard ==")
    if report:
        for k, v in report.items():
            print(f"  {k}: {v}")
        if report["crash"]:
            m = re.search(r"\+0x([0-9a-fA-F]+)", report["crash"])
            print(f"  SIGNATURE: 0x80000003 @ +0x{m.group(1) if m else '?'}"
                  "  (match against docs/known-signatures.md)")
    if logres:
        print("  layer log:")
        for k, v in logres.items():
            print(f"    {k}: {v}")
    if not report and not logres:
        print("  no recognizable xcl logs found in", a.logs)
        sys.exit(2)

if __name__ == "__main__":
    main()
