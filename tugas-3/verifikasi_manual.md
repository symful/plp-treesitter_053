# Tugas 3 - Verifikasi manual terhadap keluaran query

Berkas ini mencatat hitungan manual pada `contoh_q.py` dan `contoh_panjang.py`,
lalu membandingkannya dengan keluaran program. Tujuannya supaya angka di
laporan bisa diperiksa tanpa menjalankan apa pun.

## Cara menghitung manual

```bat
cd tugas-3
python q.py contoh_q.py fungsi.scm
python q.py contoh_q.py print.scm
python q.py contoh_q.py import.scm
python rekap_fungsi.py contoh_q.py
python q.py ..\tugas-2\contoh_panjang.py docstring.scm
```

Untuk hitungan manual, saya membaca file dengan nomor baris (`Get-Content`
atau editor) dan mencatat setiap nama fungsi, pemanggilan `print`, pernyataan
`import`, dan docstring. Hasilnya dibandingkan dengan `output/t3_*.txt`.

## Fungsi dan jumlah parameter - `contoh_q.py`

| Baris | Nama | Parameter manual | Hasil program |
| --- | --- | --- | --- |
| 6 | `sapaan` | `nama` = 1 | 1 |
| 11 | `rata_rata` | `angka` = 1 | 1 |
| 18 | `simpan` | `teks`, `berkas`, `mode` = 3 | 3 |
| 25 | `__init__` | `self`, `judul`, `penulis` = 3 | 3 |
| 29 | `tampil` | `self` = 1 | 1 |
| 33 | `contoh_import` | tidak ada = 0 | 0 |

Jumlah fungsi: **6**. Jumlah parameter: 1 + 1 + 3 + 3 + 1 + 0 = **9**.
Keluaran program ada di `output/t3_rekap_fungsi.txt` dan `output/t3_fungsi.txt`.

## Pemanggilan `print` - `contoh_q.py`

| Baris | Argumen |
| --- | --- |
| 7 | `"Halo", nama` |
| 13 | `"Data kosong"` |
| 19 | `"menyimpan", berkas` |
| 30 | `self.judul, "oleh", self.penulis` |
| 35 | `os.getcwd()` |
| 36 | `sys.version` |
| 37 | `jalur.exists()` |

Jumlah manual: **7**. Hasil query: **7** (`output/t3_print.txt`).

## Import dan nama modul - `contoh_q.py`

| Baris | Pernyataan | Modul |
| --- | --- | --- |
| 1 | `import os` | `os` |
| 2 | `import sys` | `sys` |
| 3 | `from pathlib import Path` | `pathlib` |

Jumlah manual: **3 modul**. Hasil query: **3** (`output/t3_import.txt`).

## Docstring - `contoh_panjang.py`

| Baris | Pemilik | Isi (dipotong) |
| --- | --- | --- |
| 1 | modul | `"""Modul kecil untuk mengolah data penjualan toko.` |
| 16 | kelas `Baris` | `"""Satu baris data penjualan."""` |
| 33 | kelas `Rekap` | `"""Kumpulan baris penjualan beserta perhitungannya."""` |
| 77 | fungsi `baca_csv` | `"""Baca file CSV dengan kolom tanggal, kasir, barang, jumlah, harga."""` |

Jumlah manual: **4**. Hasil query: **4** (`output/t3_docstring_panjang.txt`).

## Ringkasan

| Yang dihitung | Manual | Program | Cocok |
| --- | --- | --- | --- |
| Fungsi/method di `contoh_q.py` | 6 | 6 | ya |
| Pemanggilan `print` di `contoh_q.py` | 7 | 7 | ya |
| Nama modul di `contoh_q.py` | 3 | 3 | ya |
| Docstring di `contoh_panjang.py` | 4 | 4 | ya |

Catatan: `named_child_count` pada node `parameters` menghitung parameter
bernama, jadi parameter dengan nilai bawaan seperti `mode="w"` tetap terhitung
satu. Metode di dalam kelas ikut terhitung karena query `function_definition`
tidak membedakan fungsi biasa dan method.
