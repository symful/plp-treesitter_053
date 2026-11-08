import os
import sys
from pathlib import Path


def sapaan(nama):
    print("Halo", nama)
    return nama


def rata_rata(angka):
    if len(angka) == 0:
        print("Data kosong")
        return 0
    return sum(angka) / len(angka)


def simpan(teks, berkas, mode="w"):
    print("menyimpan", berkas)
    with open(berkas, mode) as f:
        f.write(teks)


class Laporan:
    def __init__(self, judul, penulis):
        self.judul = judul
        self.penulis = penulis

    def tampil(self):
        print(self.judul, "oleh", self.penulis)


def contoh_import():
    jalur = Path("data.txt")
    print(os.getcwd())
    print(sys.version)
    print(jalur.exists())
