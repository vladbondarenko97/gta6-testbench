#!/usr/bin/env python3
"""Analyze XCL frame dumps (frame_<n>.bmp) for the first non-black frame.

Usage: analyze_frames.py <folder-with-frame_bmps>
Prints per-frame: non-black pixel count, mean RGB, distinct color count.
Verdict line: FIRST-NON-BLACK frame index, or ALL-BLACK.
"""
import os, struct, sys
from collections import Counter

def read_bmp(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"BM":
        raise ValueError("not BMP")
    pix_off = struct.unpack_from("<I", data, 10)[0]
    hdr_sz = struct.unpack_from("<I", data, 14)[0]
    w, h = struct.unpack_from("<ii", data, 18)
    bpp = struct.unpack_from("<H", data, 28)[0]
    comp = struct.unpack_from("<I", data, 30)[0]
    if comp not in (0, 3):
        raise ValueError(f"unsupported compression {comp}")
    row = ((w * bpp // 8) + 3) & ~3
    px = data[pix_off:]
    out = []
    for y in range(abs(h)):
        base = y * row
        for x in range(w):
            o = base + x * (bpp // 8)
            b, g, r = px[o], px[o + 1], px[o + 2]
            out.append((r, g, b))
    return w, abs(h), out

def main():
    folder = sys.argv[1]
    frames = sorted(
        (f for f in os.listdir(folder) if f.startswith("frame_") and f.endswith(".bmp")),
        key=lambda f: int(f[6:-4]) if f[6:-4].isdigit() else 0,
    )
    if not frames:
        print("no frame dumps found in", folder)
        return
    first_non_black = None
    for name in frames[:60]:
        try:
            w, h, px = read_bmp(os.path.join(folder, name))
        except Exception as e:
            print(f"{name}: unreadable ({e})")
            continue
        n = len(px)
        nonblack = sum(1 for r, g, b in px if r > 8 or g > 8 or b > 8)
        mr = sum(p[0] for p in px) // n
        mg = sum(p[1] for p in px) // n
        mb = sum(p[2] for p in px) // n
        colors = len(Counter(px))
        flag = ""
        if nonblack > n * 0.01 and colors > 8:
            flag = "  << NON-BLACK"
            if first_non_black is None:
                first_non_black = name
        print(f"{name}: {w}x{h} nonblack={nonblack}/{n} ({100*nonblack/n:.2f}%) mean=({mr},{mg},{mb}) colors={colors}{flag}")
    print()
    if first_non_black:
        print(f"VERDICT: FIRST-NON-BLACK = {first_non_black}")
    else:
        print("VERDICT: ALL DUMPS BLACK (or unreadable)")

if __name__ == "__main__":
    main()
