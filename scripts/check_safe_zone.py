#!/usr/bin/env python3
r"""Checagem mecânica de zona segura para legendas ASS em 9:16 (1080x1920).

Uso: python3 scripts/check_safe_zone.py legenda.ass [--top 270 --bottom 1250 --left 80 --right 940]
Sai com 0 quando tudo está dentro da faixa, 1 quando algo invade. Valores padrão: memory/permanent.md §5.1.
Verifica: PlayRes, Alignment/MarginV/MarginL/MarginR de cada Style, e qualquer \pos(x,y) nos diálogos.
"""
import re, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("ass")
ap.add_argument("--top", type=int, default=270)
ap.add_argument("--bottom", type=int, default=1250)
ap.add_argument("--left", type=int, default=80)
ap.add_argument("--right", type=int, default=940)
ap.add_argument("--fontsize-fallback", type=int, default=80)
a = ap.parse_args()

txt = open(a.ass, encoding="utf-8", errors="replace").read()
problems = []

m = re.search(r"^PlayResX:\s*(\d+)", txt, re.M); resx = int(m.group(1)) if m else None
m = re.search(r"^PlayResY:\s*(\d+)", txt, re.M); resy = int(m.group(1)) if m else None
if (resx, resy) != (1080, 1920):
    problems.append(f"PlayRes é {resx}x{resy}; esperado 1080x1920 (os limites abaixo assumem esse canvas)")

fmt = re.search(r"^\[V4\+? Styles\].*?^Format:\s*(.+)$", txt, re.M | re.S)
styles = {}
if fmt:
    cols = [c.strip() for c in fmt.group(1).split(",")]
    for line in re.findall(r"^Style:\s*(.+)$", txt, re.M):
        vals = [v.strip() for v in line.split(",")]
        st = dict(zip(cols, vals))
        styles[st.get("Name", "?")] = st
        try:
            align = int(st.get("Alignment", 2)); mv = int(st.get("MarginV", 0))
            ml = int(st.get("MarginL", 0)); mr = int(st.get("MarginR", 0)); fs = int(float(st.get("Fontsize", a.fontsize_fallback)))
        except ValueError:
            problems.append(f"Style {st.get('Name')}: campos numéricos inválidos"); continue
        if align in (1, 2, 3):      # inferior
            baseline = 1920 - mv; top_edge = baseline - fs
            if baseline > a.bottom: problems.append(f"Style {st['Name']}: base da legenda em Y={baseline} > limite inferior {a.bottom} (MarginV={mv})")
            if top_edge < a.top: problems.append(f"Style {st['Name']}: topo da legenda em Y={top_edge} < limite superior {a.top}")
        elif align in (7, 8, 9):    # superior
            if mv < a.top: problems.append(f"Style {st['Name']}: alinhado ao topo com MarginV={mv} < {a.top}")
        if ml < a.left: problems.append(f"Style {st['Name']}: MarginL={ml} < {a.left}")
        if 1080 - mr > a.right: problems.append(f"Style {st['Name']}: MarginR={mr} deixa texto até X={1080-mr} > {a.right}")

for ln, line in enumerate(txt.splitlines(), 1):
    if not line.startswith("Dialogue:"): continue
    for x, y in re.findall(r"\\pos\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", line):
        x, y = float(x), float(y)
        if not (a.left <= x <= a.right and a.top <= y <= a.bottom):
            problems.append(f"linha {ln}: \\pos({x:.0f},{y:.0f}) fora da faixa X[{a.left},{a.right}] Y[{a.top},{a.bottom}]")

if problems:
    print("SAFE ZONE: FALHOU"); [print(" -", p) for p in problems]; sys.exit(1)
print(f"SAFE ZONE: OK ({len(styles)} style(s), limites Y[{a.top},{a.bottom}] X[{a.left},{a.right}])")
