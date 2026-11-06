import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Tugas 1 - Membaca pohon
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

parser = Parser(Language(tspython.language()))

berkas = sys.argv[1]
with open(berkas, "rb") as f:
    tree = parser.parse(f.read())

print("=== Pohon ===")
print(tree.root_node)

print()
print("=== Anak bernama root ===")
for anak in tree.root_node.named_children:
    print(anak.type)
