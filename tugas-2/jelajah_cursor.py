import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Tugas 2 (pengayaan) - penjelajah dengan TreeCursor
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

parser = Parser(Language(tspython.language()))


def jelajah(node):
    cursor = node.walk()
    kedalaman = 0
    while True:
        sekarang = cursor.node
        if sekarang.is_named:
            baris, kolom = sekarang.start_point
            label = f"{cursor.field_name}: " if cursor.field_name else ""
            print("  " * kedalaman + f"{label}{sekarang.type} [{baris + 1}:{kolom}]")
            if cursor.goto_first_child():
                kedalaman += 1
                continue
        while True:
            if cursor.goto_next_sibling():
                break
            if not cursor.goto_parent():
                return
            kedalaman -= 1


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)
