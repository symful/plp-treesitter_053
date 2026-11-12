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
print("=== Anak langsung root ===")
for anak in tree.root_node.children:
    tanda = "bernama" if anak.is_named else "anonim"
    print(anak.type, tanda)

# Pilih node pertama yang punya anak anonim supaya perbedaan children dan
# named_children terlihat langsung: pada function_definition, "def" dan ":"
# hanya muncul di children, sedangkan named_children melewatinya.
kandidat = next(
    (n for n in tree.root_node.named_children
     if any(not anak.is_named for anak in n.children)),
    tree.root_node.named_children[0],
)

print()
print("=== children vs named_children ===")
print("node:", kandidat.type)

print(f"children ({len(kandidat.children)}):")
for i, anak in enumerate(kandidat.children):
    field = kandidat.field_name_for_child(i)
    label = f", field={field}" if field else ""
    tanda = "bernama" if anak.is_named else "anonim"
    print(f"  [{i}] {anak.type} ({tanda}{label})")

print(f"named_children ({len(kandidat.named_children)}):")
for i, anak in enumerate(kandidat.named_children):
    print(f"  [{i}] {anak.type}")

print()
print("=== Status error ===")
print("has_error:", tree.root_node.has_error)
