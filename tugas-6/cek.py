import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

# Tugas 6 - Pemeriksa TODO, fungsi panjang, dan file error
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

LEWATI = {"venv", ".venv", ".git", "node_modules", "__pycache__", "build"}


def cek_file(path):
    tree = parser.parse(path.read_bytes())

    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: TODO {teks}")


for path in Path(sys.argv[1]).rglob("*.py"):
    if LEWATI & set(path.parts):
        continue
    cek_file(path)
