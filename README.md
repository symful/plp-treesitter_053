# Praktikum Tree-sitter

Kemal Ardian (251524053), Kelas 2B, D-4 Teknik Informatika, Politeknik Negeri Bandung.
Mata kuliah Programming Language Pragmatics.

Repositori: https://github.com/symful/plp-treesitter_053

## Isi folder

| Folder / berkas | Isi |
| --- | --- |
| `tugas-1/` | Membaca pohon: `t1.py`, tiga potongan kode dan versi rusaknya, keluaran di `output/` |
| `tugas-2/` | Penjelajah node: `jelajah.py`, versi `TreeCursor`, `contoh_panjang.py`, keluaran di `output/` |
| `tugas-3/` | Query: `q.py`, `rekap_fungsi.py`, lima query `.scm`, keluaran di `output/` |
| `tugas-4/` | Grammar DSL filter di `tree-sitter-filter/`, ditambah `filter_sql.py` untuk pengayaan WHERE berparameter |
| `tugas-5/` | `highlights.scm` yang dipasang di proyek tugas-4, beserta catatan capture-nya |
| `tugas-6/` | `cek.py`, folder `uji/`, `hasil_repo.txt`, dan README cara pakai |
| `demo/` | Skrip `.bat` untuk menjalankan ulang tiap tugas saat demo |
| `dokumentasi/` | Tangkapan layar hasil tiap tugas yang dipakai di laporan |
| `Laporan_PLP_2B_053.docx` | Laporan praktikum (tiga halaman isi) |
| `LAPORAN.md` | Laporan dalam bentuk Markdown, lengkap dengan tangkapan layar dan catatan penggunaan AI |
| `Proposal_Draf_PLP_2B_053.docx` | Draf proposal proyek (satu halaman) |
| `LINK_REPO.md` | Ringkasan isi repositori untuk pengumpulan |

## Lingkungan yang dipakai

Windows 11, Python 3.12, tree-sitter 0.26 dan tree-sitter-python 0.25,
tree-sitter CLI 0.27.2, Node.js 22, serta g++ MinGW untuk mengompilasi parser.

```bat
python -m venv .venv
.venv\Scripts\activate
pip install tree-sitter tree-sitter-python
```

## Menjalankan Tugas 1 sampai 3

```bat
cd tugas-1
python t1.py potongan1.py
python t1.py potongan1_rusak.py

cd ..\tugas-2
python jelajah.py contoh_panjang.py
python jelajah_cursor.py contoh_panjang.py

cd ..\tugas-3
python q.py contoh_q.py print.scm
python rekap_fungsi.py contoh_q.py
```

Keluaran yang tersimpan ada di `output/` pada tiap folder tugas.

## Menjalankan Tugas 4 dan 5

`src/grammar.json` dan `src/node-types.json` tidak disimpan karena hasil generate,
jadi jalankan `tree-sitter generate` lebih dulu sebelum `test`.

```bat
cd tugas-4\tree-sitter-filter
tree-sitter generate
tree-sitter test
tree-sitter highlight contoh.filter
tree-sitter parse contoh2.filter
tree-sitter build --output ..\filter.dll
python ..\filter_sql.py contoh.filter
```

`filter.dll` yang sudah jadi ikut disimpan di `tugas-4/` supaya `filter_sql.py`
bisa langsung dipakai tanpa mengompilasi ulang. Query highlight ada di
`queries/highlights.scm`, salinannya di `tugas-5/highlights.scm`.

## Menjalankan Tugas 6

```bat
cd tugas-6
python cek.py uji
python cek.py C:\temp\requests
```
