import re
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

# Console Windows kadang memakai cp1252, yang tidak bisa mencetak karakter
# pengganti (U+FFFD) hasil decode file non-UTF-8. Paksa keluaran UTF-8 dan
# ganti karakter yang tetap tidak bisa ditulis, jangan sampai skrip berhenti.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_KOMENTAR = Query(PY, '(comment) @c')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

LEWATI = {"venv", ".venv", ".git", "node_modules", "__pycache__", "build"}


def komentar_todo(tree):
    """Ambil komentar TODO/FIXME.

    Predikat #match? mendekode teks node sebagai UTF-8. Pada berkas latin-1,
    dekode itu melempar UnicodeDecodeError sebelum kita sempat mencetak apa pun.
    Kalau itu terjadi, query cadangan mengambil semua komentar lalu menyaring
    teksnya dengan errors="replace".
    """
    try:
        yield from QueryCursor(Q_TODO).captures(tree.root_node).get("c", [])
    except UnicodeDecodeError:
        for node in QueryCursor(Q_KOMENTAR).captures(tree.root_node).get("c", []):
            teks = node.text.decode(errors="replace")
            if re.search(r"TODO|FIXME", teks):
                yield node


def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for anak in node.children:
        hasil = cari_error(anak)
        if hasil:
            return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())

    for node in komentar_todo(tree):
        teks = node.text.decode(errors="replace").strip()
        jenis = "FIXME" if "FIXME" in teks else "TODO"
        print(f"{path}:{node.start_point[0] + 1}: {jenis} {teks}")

    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        baris = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if baris > 30:
            print(f"{path}:{fungsi.start_point[0] + 1}: PANJANG {nama} {baris} baris")

    if tree.root_node.has_error:
        salah = cari_error(tree.root_node)
        print(f"{path}:{salah.start_point[0] + 1}: ERROR sintaks {salah.type}")


target = Path(sys.argv[1])
if target.is_file():
    berkas = [target]
else:
    berkas = [p for p in target.rglob("*.py") if not (LEWATI & set(p.parts))]

for path in berkas:
    cek_file(path)
