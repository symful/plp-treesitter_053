import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

# Tugas 3 - Penjalan query
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

hasil = QueryCursor(Query(PY, pola)).captures(tree.root_node)
for nama, nodes in hasil.items():
    for n in nodes:
        print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")
