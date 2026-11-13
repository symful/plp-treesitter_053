# cek.py - pemeriksa kode Python berbasis tree-sitter

Skrip ini mem-parse setiap file `.py` di sebuah folder (atau satu file), lalu
melaporkan tiga hal:

1. komentar yang memuat `TODO` atau `FIXME`,
2. fungsi yang panjangnya lebih dari 30 baris, dihitung dari baris `def` sampai
   baris terakhir badan fungsi (baris `def` ikut dihitung),
3. file yang pohon sintaksnya mengandung error.

## Pasang dependensi

```bash
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```bash
python cek.py uji
python cek.py uji\latin1.py
python cek.py C:\path\ke\repo
```

Folder `venv`, `.venv`, `.git`, `node_modules`, `__pycache__`, dan `build`
dilewati supaya pemeriksaan tetap cepat.

## Contoh output

```text
uji\latin1.py:2: TODO # TODO: nama berkas caf? sudah usang
uji\panjang.py:1: PANJANG hitung_rekap 31 baris
uji\rusak.py:1: ERROR sintaks ERROR
uji\todo.py:10: TODO # TODO: tambahkan penanganan berkas kosong
uji\todo.py:13: FIXME # FIXME: belum menutup berkas kalau terjadi error
```

Format barisnya `file:baris: jenis temuan`. Tanda `?` pada `caf?` adalah
pengganti byte `0xE9` dari berkas latin-1; lihat bagian berikut.

## Catatan

- Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- Panjang dihitung dari baris `def` sampai baris terakhir badan fungsi.
- Untuk file yang error, yang dilaporkan adalah node bermasalah pertama
  (`ERROR` atau `MISSING`) yang ditemukan saat menelusuri pohon.
- Kalau argumennya satu file, hanya file itu yang diperiksa; kalau folder,
  pemeriksaan dilakukan rekursif.

## Berkas non-UTF-8

`uji/latin1.py` sengaja disimpan sebagai latin-1 dan memuat byte `0xE9` pada
komentar TODO serta string. Berkas ini menguji dua lapisan:

1. Predikat `#match?` di query mendekode teks node sebagai UTF-8, sehingga
   berkas latin-1 melempar `UnicodeDecodeError` sebelum komentar sempat dicetak.
   `cek.py` menangkap error itu dan memakai query cadangan `(comment) @c`,
   lalu menyaring teksnya di Python dengan `re.search`.
2. `sys.stdout` di Windows bisa memakai cp1252 yang tidak bisa menulis karakter
   pengganti `U+FFFD`. Karena itu keluaran diubah ke UTF-8 dengan
   `errors="replace"` agar skrip tidak berhenti saat mencetak.

Dengan dua penanganan itu, `python cek.py uji` tetap selesai dan melaporkan
TODO dari berkas latin-1, bukan berhenti dengan traceback. Ini juga alasan
`node.text.decode(errors="replace")` saja tidak cukup: penggantian saat decode
tidak menolong kalau kegagalannya terjadi di dalam predikat query.

## Hasil uji pada repo nyata

`hasil_repo.txt` adalah hasil menjalankan perintah berikut pada 26 Oktober 2026:

```bat
git clone https://github.com/psf/requests C:\temp\requests
cd C:\temp\requests
git rev-parse HEAD
python cek.py C:\temp\requests
```

Repo uji: [psf/requests](https://github.com/psf/requests), commit
**`3c7baaa05ab4aa49cc819ce3a819d260de19c157`** (26 Oktober 2026), 37 file `.py`.

Hasil:

- 7 temuan TODO/FIXME. Hitungan manual dengan
  `grep -rn --include=*.py -E '#.*(TODO|FIXME)'` (peka huruf besar-kecil)
  juga menghasilkan 7 baris.
- 56 fungsi lebih dari 30 baris.
- Tidak ada file yang gagal di-parse.

### Pemeriksaan manual dua file

| File | Fungsi | Baris | Panjang manual | Hasil `cek.py` |
| --- | --- | --- | --- | --- |
| `src/requests/utils.py` | `super_len` | 160–228 | 228 − 160 + 1 = **69** | 69 baris |
| `src/requests/models.py` | `prepare_url` | 483–563 | 563 − 483 + 1 = **81** | 81 baris |

Cara memeriksa: buka file dengan nomor baris, cari baris `def`, lalu hitung
sampai baris terakhir sebelum `def` berikutnya. Untuk `super_len`, baris 160
adalah `def super_len(o: Any) -> int:` dan baris 228 adalah
`return max(0, total_length - current_position)`. Untuk `prepare_url`, baris
483 adalah `def prepare_url(` dan baris 563 adalah `self.url = url`. Keduanya
cocok dengan keluaran `cek.py` pada `hasil_repo.txt`.

### Kenapa `super_len` penting

`super_len` adalah kasus yang membuktikan rumus `end_point[0] - start_point[0] + 1`
benar. Tanpa `+1`, fungsinya terbaca 68 baris, bukan 69. Selisih satu baris itu
yang membuat pemeriksaan manual perlu dilakukan, bukan sekadar percaya pada
keluaran program.
