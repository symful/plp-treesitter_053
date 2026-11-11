# cek.py — pemeriksa kode Python berbasis tree-sitter

Skrip ini mem-parse setiap file `.py` di sebuah folder, lalu melaporkan tiga hal:

1. komentar yang memuat `TODO` atau `FIXME`,
2. fungsi yang panjang badannya lebih dari 30 baris,
3. file yang pohon sintaksnya mengandung error.

## Pasang dependensi

```bash
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```bash
python cek.py uji
python cek.py C:\path\ke\repo
```

Folder `venv`, `.venv`, `.git`, `node_modules`, `__pycache__`, dan `build`
dilewati supaya pemeriksaan tetap cepat.

## Contoh output

```
uji\panjang.py:1: PANJANG hitung_rekap 31 baris
uji\rusak.py:1: ERROR sintaks ERROR
uji\todo.py:10: TODO # TODO: tambahkan penanganan berkas kosong
uji\todo.py:13: TODO # FIXME: belum menutup berkas kalau terjadi error
```

Format barisnya `file:baris: jenis temuan`.

## Catatan

- Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- Panjang dihitung dari baris `def` sampai baris terakhir badan fungsi.
- Untuk file yang error, yang dilaporkan adalah node bermasalah pertama
  (`ERROR` atau `MISSING`) yang ditemukan saat menelusuri pohon.

## Hasil uji pada repo nyata

`hasil_repo.txt` adalah hasil menjalankan `python cek.py C:\temp\requests` pada repo
[psf/requests](https://github.com/psf/requests) (37 file `.py`):

- 7 temuan TODO, sama dengan hasil `grep -rn --include=*.py -E "#.*(TODO|FIXME)"`
  pada repo yang sama,
- 56 fungsi lebih dari 30 baris, misalnya `super_len` di `src/requests/utils.py`
  baris 160 sampai 228 (69 baris),
- tidak ada file yang gagal di-parse.
