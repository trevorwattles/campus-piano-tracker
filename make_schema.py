"""Draw schema.png from setup.sql (needs Graphviz: `brew install graphviz`)."""
import html
import os
import sqlite3
import subprocess

here = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(":memory:")
con.executescript(open(os.path.join(here, "setup.sql")).read())
tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' order by rowid")]

lines = [
    "digraph schema {",
    '  graph [rankdir=LR, splines=spline, nodesep=0.5, ranksep=1.1, pad=0.3, bgcolor="white",'
    ' label="Campus Piano Tracker", labelloc=t, fontsize=20, fontname="Helvetica-Bold"];',
    '  node [shape=plain, fontname="Helvetica", fontsize=11];',
    '  edge [arrowhead=crowodot, arrowtail=teetee, dir=both, color="#555555"];',
]

for t in tables:
    cols = con.execute(f"pragma table_info({t})").fetchall()  # cid, name, type, notnull, default, pk
    fks = {r[3] for r in con.execute(f"pragma foreign_key_list({t})")}
    rows = [f'<tr><td colspan="3" bgcolor="#f0e2b6" align="left"><b>{t}</b></td></tr>']
    for _, name, ctype, notnull, _, pk in cols:
        key = "PK" if pk else ("FK" if name in fks else "")
        label = f"<b><u>{name}</u></b>" if pk else name
        null = " NOT NULL" if notnull and not pk else ""
        rows.append(
            f'<tr><td port="{name}_in" align="left">{label}</td>'
            f'<td align="left"><font color="#555555">{html.escape(ctype.upper())}{null}</font></td>'
            f'<td port="{name}_out" align="left">{f"<font color=\"#8a5a00\">{key}</font>" if key else " "}</td></tr>'
        )
    lines.append(
        f'  {t} [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="4" color="#999999">'
        + "".join(rows) + "</table>>];"
    )

for t in tables:
    for _, _, ref_table, from_col, to_col, *_ in con.execute(f"pragma foreign_key_list({t})"):
        # one parent row -> many child rows
        lines.append(f"  {ref_table}:{to_col}_out:e -> {t}:{from_col}_in:w;")
lines.append("}")

out = os.path.join(here, "schema.png")
subprocess.run(["dot", "-Tpng", "-Gdpi=150", "-o", out], input="\n".join(lines), text=True, check=True)
print("wrote", out)
