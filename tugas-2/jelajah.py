import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Tugas 2 - Penjelajah node
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, anak in enumerate(node.children):
        if anak.is_named:
            jelajah(anak, kedalaman + 1, node.field_name_for_child(i))


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)
