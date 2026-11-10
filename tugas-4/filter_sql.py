import ctypes
import os
import sys
from ctypes import c_char_p, c_void_p, py_object
from pathlib import Path

from tree_sitter import Language, Parser

# Tugas 4 (pengayaan) - mengubah pohon DSL filter menjadi klausa WHERE
# Nama  : Kemal Ardian
# NIM   : 251524053
# Kelas : 2B

lib_path = Path(__file__).with_name("filter.dll" if os.name == "nt" else "filter.so")
lib = ctypes.cdll.LoadLibrary(str(lib_path))
lib.tree_sitter_filter.restype = c_void_p
ptr = lib.tree_sitter_filter()

# tree_sitter_filter() mengembalikan pointer ke struct TSLanguage.
# py-tree-sitter menerimanya sebagai PyCapsule bernama tree_sitter.Language.
PyCapsule_New = ctypes.pythonapi.PyCapsule_New
PyCapsule_New.restype = py_object
PyCapsule_New.argtypes = [c_void_p, c_char_p, c_void_p]
kapsul = PyCapsule_New(c_void_p(ptr), b"tree_sitter.Language", None)

FILTER = Language(kapsul)
parser = Parser(FILTER)

OP = {"=": "=", "!=": "<>", ">": ">", "<": "<", ">=": ">=", "<=": "<="}


def nilai(node, params):
    """Kembalikan placeholder dan tambahkan nilainya ke daftar parameter."""
    teks = node.text.decode()
    if node.type == "string":
        params.append(teks[1:-1])
    elif node.type == "number":
        params.append(float(teks) if "." in teks else int(teks))
    elif node.type == "boolean":
        params.append(1 if teks == "true" else 0)
    return "?"


def ke_sql(node, params):
    tipe = node.type
    if tipe == "comparison":
        kolom = node.child_by_field_name("field").text.decode()
        operator = OP[node.child_by_field_name("operator").text.decode()]
        kanan = nilai(node.child_by_field_name("value"), params)
        return f"{kolom} {operator} {kanan}"
    if tipe == "in_expression":
        kolom = node.child_by_field_name("field").text.decode()
        daftar = node.child_by_field_name("values")
        isi = [nilai(v, params) for v in daftar.named_children]
        return f"{kolom} IN ({', '.join(isi)})"
    if tipe == "contains_expression":
        kolom = node.child_by_field_name("field").text.decode()
        kanan = nilai(node.child_by_field_name("value"), params)
        return f"{kolom} LIKE '%' || {kanan} || '%'"
    if tipe == "and_expression":
        kiri = ke_sql(node.child_by_field_name("left"), params)
        kanan = ke_sql(node.child_by_field_name("right"), params)
        return f"({kiri} AND {kanan})"
    if tipe == "or_expression":
        kiri = ke_sql(node.child_by_field_name("left"), params)
        kanan = ke_sql(node.child_by_field_name("right"), params)
        return f"({kiri} OR {kanan})"
    if tipe == "not_expression":
        isi = ke_sql(node.child_by_field_name("operand"), params)
        return f"NOT ({isi})"
    if tipe == "parenthesized":
        return ke_sql(node.named_children[0], params)
    raise ValueError(f"node tidak dikenal: {tipe}")


teks = open(sys.argv[1]).read()
tree = parser.parse(teks.encode())

if tree.root_node.has_error:
    print("query tidak valid")
    sys.exit(1)

params = []
where = ke_sql(tree.root_node.named_children[0], params)
print("SQL  : SELECT * FROM tickets WHERE " + where)
print("param:", params)
