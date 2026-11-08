import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

# Tugas 3 - Rekap nama fungsi dan jumlah parameter
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
tree = parser.parse(kode)

pola = """
(function_definition
  name: (identifier) @nama
  parameters: (parameters) @params)
"""
query = Query(PY, pola)

print("nama fungsi | jumlah parameter")
for _, cap in QueryCursor(query).matches(tree.root_node):
    nama = cap["nama"][0].text.decode()
    jumlah = cap["params"][0].named_child_count
    print(f"{nama} | {jumlah}")
