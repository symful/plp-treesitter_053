import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Tugas 1 - Membaca pohon
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

parser = Parser(Language(tspython.language()))

kode = b"x = 1\n"
tree = parser.parse(kode)
print(tree.root_node)
