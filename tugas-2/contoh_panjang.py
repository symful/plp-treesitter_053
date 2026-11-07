"""Modul kecil untuk mengolah data penjualan toko.

Dipakai di tugas kuliah: membaca data penjualan dari file CSV sederhana,
menghitung total, lalu menampilkan ringkasan per kasir.

Nama  : Kemal Ardian
NIM   : 251524053
Kelas : 2B
"""

import csv
from datetime import date


class Baris:
    """Satu baris data penjualan."""

    def __init__(self, tanggal, kasir, barang, jumlah, harga):
        self.tanggal = tanggal
        self.kasir = kasir
        self.barang = barang
        self.jumlah = jumlah
        self.harga = harga

    def total(self):
        return self.jumlah * self.harga

    def __repr__(self):
        return f"Baris({self.kasir}, {self.barang}, {self.jumlah})"


class Rekap:
    """Kumpulan baris penjualan beserta perhitungannya."""

    def __init__(self):
        self.baris = []

    def tambah(self, baris):
        if baris.jumlah <= 0:
            raise ValueError("jumlah harus lebih dari nol")
        if baris.harga < 0:
            raise ValueError("harga tidak boleh negatif")
        self.baris.append(baris)

    def total_semua(self):
        total = 0
        for baris in self.baris:
            total = total + baris.total()
        return total

    def total_per_kasir(self):
        hasil = {}
        for baris in self.baris:
            if baris.kasir in hasil:
                hasil[baris.kasir] = hasil[baris.kasir] + baris.total()
            else:
                hasil[baris.kasir] = baris.total()
        return hasil

    def barang_terlaris(self):
        jumlah = {}
        for baris in self.baris:
            if baris.barang in jumlah:
                jumlah[baris.barang] = jumlah[baris.barang] + baris.jumlah
            else:
                jumlah[baris.barang] = baris.jumlah
        terlaris = None
        terbanyak = 0
        for nama, banyak in jumlah.items():
            if banyak > terbanyak:
                terlaris = nama
                terbanyak = banyak
        return terlaris, terbanyak


def baca_csv(path):
    """Baca file CSV dengan kolom tanggal, kasir, barang, jumlah, harga."""
    rekap = Rekap()
    with open(path, newline="", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        for row in pembaca:
            tahun, bulan, hari = [int(x) for x in row["tanggal"].split("-")]
            baris = Baris(
                date(tahun, bulan, hari),
                row["kasir"],
                row["barang"],
                int(row["jumlah"]),
                int(row["harga"]),
            )
            rekap.tambah(baris)
    return rekap


def cetak_ringkasan(rekap):
    print("Total penjualan:", rekap.total_semua())
    print()
    print("Per kasir:")
    for kasir, total in sorted(rekap.total_per_kasir().items()):
        print(" ", kasir, "=", total)
    nama, banyak = rekap.barang_terlaris()
    print()
    print("Barang terlaris:", nama, "sebanyak", banyak, "unit")


def main():
    rekap = Rekap()
    rekap.tambah(Baris(date(2026, 10, 1), "Budi", "Kopi", 3, 15000))
    rekap.tambah(Baris(date(2026, 10, 1), "Sari", "Teh", 2, 8000))
    rekap.tambah(Baris(date(2026, 10, 2), "Budi", "Kopi", 5, 15000))
    rekap.tambah(Baris(date(2026, 10, 2), "Sari", "Roti", 4, 12000))
    cetak_ringkasan(rekap)


if __name__ == "__main__":
    main()
