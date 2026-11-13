# Praktikum Tree-sitter

Kemal Ardian (251524053), Kelas 2B, D-4 Teknik Informatika, Politeknik Negeri Bandung.
Mata kuliah Programming Language Pragmatics.

Repositori: <https://github.com/symful/plp-treesitter_053>

## Isi folder

| Folder / berkas | Isi |
| --- | --- |
| `tugas-1/` | `t1.py`, tiga potongan dan versi rusaknya, `pohon_perkiraan.md`, keluaran di `output/` |
| `tugas-2/` | `jelajah.py`, `jelajah_cursor.py`, `contoh_panjang.py`, keluaran di `output/` |
| `tugas-3/` | `q.py`, `rekap_fungsi.py`, lima query `.scm`, `verifikasi_manual.md`, keluaran di `output/` |
| `tugas-4/` | Grammar DSL filter di `tree-sitter-filter/`, `filter_sql.py`, `filter.dll` |
| `tugas-5/` | `highlights.scm`, README setup, bukti query di `output/` |
| `tugas-6/` | `cek.py`, folder `uji/`, `hasil_repo.txt`, README, keluaran di `output/` |
| `demo/` | Skrip `.bat` untuk menjalankan ulang tiap tugas |
| `LAPORAN.md` | Laporan teks lengkap, tanpa gambar |
| `Laporan_PLP_2B_053.docx` | Laporan versi template, tiga halaman total |
| `Laporan_PLP_2B_053.pdf` | Laporan tiga halaman, keluaran teks |
| `Proposal_Draf_PLP_2B_053.md` | Draf proposal satu halaman |
| `Proposal_Draf_PLP_2B_053.docx` | Draf proposal versi Word |
| `Proposal_Draf_PLP_2B_053.pdf` | Draf proposal satu halaman |
| `LINK_REPO.md` | Ringkasan isi repositori untuk pengumpulan |

## Lingkungan

Windows 11, Python 3.12, tree-sitter 0.26, tree-sitter-python 0.25,
tree-sitter-cli 0.27.2, Node.js 22, dan g++ MinGW.

```bat
python -m venv .venv-win
.venv-win\Scripts\activate
pip install tree-sitter tree-sitter-python
```

`demo\_env.bat` menghitung folder proyek dari lokasi skrip (`%~dp0..`), jadi
skrip demo bisa dipakai di komputer lain selama dependensi di atas tersedia.

## Tugas 1 sampai 3

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

## Tugas 4 dan 5

`src/grammar.json` dan `src/node-types.json` tidak disimpan karena hasil generate.

```bat
cd tugas-4\tree-sitter-filter
tree-sitter generate
tree-sitter test
tree-sitter highlight contoh.filter
tree-sitter build --output ..\filter.dll
python ..\filter_sql.py contoh.filter
```

Untuk highlight, jalankan `tree-sitter init-config` sekali, lalu isi
`parser-directories` dengan folder induk proyek, yaitu `...\tugas-4`.
Langkah lengkap ada di `tugas-5/README.md`.

## Tugas 6

```bat
cd tugas-6
python cek.py uji
python cek.py C:\temp\requests
```

Repo uji dan commit yang dipakai tercatat di `tugas-6/README.md`. Berkas
`uji/latin1.py` sengaja memakai encoding latin-1 untuk menguji penanganan
berkas non-UTF-8.

## Laporan

`LAPORAN.md` adalah versi utama dan memuat potongan keluaran sebagai teks,
bukan gambar. `Laporan_PLP_2B_053.docx` dibangun dari
`laporan/build/generate.py` dengan `content_plp.json`; PDF tiga halaman
tersedia di `Laporan_PLP_2B_053.pdf`. Batas tiga halaman total dipenuhi dengan
memakai teks, bukan tangkapan layar.
