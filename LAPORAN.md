# Laporan Praktikum Tree-sitter

Kemal Ardian (251524053), Kelas 2B, D-4 Teknik Informatika, Politeknik Negeri Bandung.
Mata kuliah Programming Language Pragmatics.

Repositori: <https://github.com/symful/plp-treesitter_053>

## Tugas 1 - Membaca pohon

`t1.py` mem-parse tiga potongan (fungsi, `if`/`else`, kelas) dan tiga versi rusaknya.
Pohon perkiraan ditulis lebih dulu, lalu hasil parser dibandingkan. Arsip perkiraan
dari pengerjaan pertama tidak ada, jadi perkiraan di bawah ditulis ulang saat bukti
ini disusun dan parser dijalankan ulang; perbedaannya dicatat apa adanya.

| Potongan | Perkiraan | Hasil parser | Selisih yang ditemukan |
| --- | --- | --- | --- |
| Fungsi | `function_definition` dengan `name`, `parameters`, `body` | sama | `string` ternyata berisi `string_start`, `string_content`, `string_end` |
| If/else | `if_statement` dengan `condition`, `consequence`, `alternative` | sama | isi `string` seperti di atas; `if`, `:`, `else` anonim |
| Kelas | `class_definition` berisi dua `function_definition` | sama | `attribute` punya field `object:` dan `attribute:` |

Hasil parser untuk potongan fungsi (diringkas dari `output/t1_potongan1.txt`):

```text
(module (function_definition name: (identifier)
  parameters: (parameters (identifier))
  body: (block
    (expression_statement (assignment left: (identifier)
      right: (binary_operator
        left: (string (string_start) (string_content) (string_end))
        right: (identifier))))
    (return_statement (identifier)))))
```

Node anonim yang tersembunyi dari S-expression: `def`, `:`, `(`, `)`, `=`, dan `if`.
`def` dan `:` tetap ada di `children`; `(` dan `)` ada di dalam node `parameters`.
Perbedaan `children` dan `named_children` dari `potongan1.py`:

```text
node: function_definition
children (5):
  [0] def (anonim)
  [1] identifier (bernama, field=name)
  [2] parameters (bernama, field=parameters)
  [3] : (anonim)
  [4] block (bernama, field=body)
named_children (3):
  [0] identifier
  [1] parameters
  [2] block
```

`children` memuat semua anak, termasuk token anonim, dan indeksnya yang dipakai
`field_name_for_child(i)`. `named_children` hanya memuat anak bernama; indeksnya
tidak sama, sehingga memakai indeks `named_children` untuk label field akan bergeser.

Tiga kode rusak menghasilkan status error:

```text
potongan1_rusak.py  (module (ERROR ...))                      has_error: True
potongan2_rusak.py  (module (ERROR (string ...)))             has_error: True
potongan3_rusak.py  (conditional_expression ... (MISSING identifier))  has_error: True
```

Pada `potongan1_rusak.py` seluruh fungsi menjadi satu `ERROR`; pada
`potongan2_rusak.py` parser tidak memakai `MISSING ")"` melainkan membungkus
`print`, `(`, dan string ke dalam `ERROR`; pada `potongan3_rusak.py` muncul
`MISSING identifier` di posisi kondisi `if` yang hilang. Bukti lengkap:
[`tugas-1/pohon_perkiraan.md`](tugas-1/pohon_perkiraan.md) dan
[`tugas-1/output/`](tugas-1/output/).

## Tugas 2 - Penjelajah node

`jelajah.py` menelusuri `node.children` dengan `enumerate`, melewati anak yang
tidak bernama, dan memakai `field_name_for_child(i)` sebagai label. Versi
`TreeCursor` menempuh pohon yang sama. Pada `contoh_panjang.py` (115 baris),
keduanya menghasilkan 681 baris yang identik; `fc` tidak menemukan perbedaan.

```text
module [1:0]
  expression_statement [1:0]
    string [1:0]
      string_start [1:0]
      string_content [1:3]
      string_end [9:0]
  import_statement [11:0]
    name: dotted_name [11:7]
```

Keluaran lengkap: [`t2_kecil.txt`](tugas-2/output/t2_kecil.txt) dan
[`t2_panjang.txt`](tugas-2/output/t2_panjang.txt).

## Tugas 3 - Query

Hitungan manual dibandingkan dengan keluaran query pada `contoh_q.py` dan
`contoh_panjang.py`:

| Yang dihitung | Manual | Program | Cocok |
| --- | --- | --- | --- |
| Fungsi/method | 6 | 6 | ya |
| Parameter (total) | 9 | 9 | ya |
| Pemanggilan `print` | 7 | 7 | ya |
| Nama modul (`os`, `sys`, `pathlib`) | 3 | 3 | ya |
| Docstring di `contoh_panjang.py` | 4 | 4 | ya |

Rincian manual ada di [`tugas-3/verifikasi_manual.md`](tugas-3/verifikasi_manual.md);
keluaran query ada di [`tugas-3/output/`](tugas-3/output/).

## Tugas 4 - Grammar DSL filter

Grammar memuat `comparison`, `in_expression`, `contains_expression`, `and`, `or`,
`not`, `parenthesized`, dan tiga jenis nilai. `prec.left` membuat `and` mengikat
lebih kuat daripada `or`. Delapan kasus uji lulus:

```text
  dasar:
      1. ✓ perbandingan sederhana
      2. ✓ and lebih kuat dari or
      3. ✓ kurung mengubah pengelompokan
      4. ✓ not dan boolean
      5. ✓ operator in dengan tiga nilai
      6. ✓ operator contains
      7. ✓ tiga jenis nilai dalam satu query
      8. ✓ nama field bertitik
Total parses: 8; successful parses: 8; failed parses: 0; success percentage: 100.00%
```

Saat semua `prec` dihapus sementara, `tree-sitter generate` berhenti dengan:

```text
Unresolved conflict for symbol sequence:
  'not'  _expr  •  'or'  …
```

Setelah `prec` dikembalikan, kedelapan tes lulus lagi. Di Windows, compiler
diarahkan dengan `set CC=gcc` sebelum `tree-sitter test`.

## Tugas 5 - Highlight

`highlights.scm` memberi capture untuk kata kunci, operator, string, angka,
boolean, nama field, dan tanda kurung. Setup CLI memakai `tree-sitter init-config`
dan `parser-directories` yang menunjuk folder induk `tugas-4` (bukan folder
`tree-sitter-filter`). Keluaran query untuk `contoh2.filter`:

```text
capture: 0 - keyword,        text: `not`
capture: 5 - property,       text: `archived`
capture: 4 - constant.builtin, text: `true`
capture: 0 - keyword,        text: `in`
capture: 2 - string,         text: `"open"`
capture: 7 - punctuation.delimiter, text: `,`
capture: 0 - keyword,        text: `contains`
```

Pengayaan `filter_sql.py` mengubah pohon menjadi `WHERE` berparameter:

```text
SQL  : SELECT * FROM tickets WHERE (status = ? AND (priority > ? OR owner = ?))
param: ['open', 2, 'budi']
```

Langkah setup lengkap ada di [`tugas-5/README.md`](tugas-5/README.md); bukti
tekstual di [`tugas-5/output/`](tugas-5/output/).

## Tugas 6 - Pemeriksa kode

`cek.py` melaporkan komentar TODO/FIXME, fungsi lebih dari 30 baris (dihitung
dari baris `def`), dan file yang pohonnya error. Pada folder `uji/`:

```text
uji\latin1.py:2: TODO # TODO: nama berkas caf? sudah usang
uji\panjang.py:1: PANJANG hitung_rekap 31 baris
uji\rusak.py:1: ERROR sintaks ERROR
uji\todo.py:10: TODO # TODO: tambahkan penanganan berkas kosong
uji\todo.py:13: FIXME # FIXME: belum menutup berkas kalau terjadi error
```

`uji/latin1.py` sengaja memakai encoding latin-1. Predikat `#match?` mendekode
teks sebagai UTF-8 dan melempar `UnicodeDecodeError`; `cek.py` menangkapnya,
memakai query cadangan `(comment) @c`, lalu menyaring dengan `re.search`.
Keluaran juga dipaksa UTF-8 karena console cp1252 tidak bisa mencetak `U+FFFD`.

Pada repo `psf/requests`, commit **`3c7baaa05ab4aa49cc819ce3a819d260de19c157`**
(26 Oktober 2026, 37 file `.py`), skrip menemukan **7 TODO/FIXME**, **56 fungsi
panjang**, dan **0 file error**. Hitungan manual `grep` juga 7. Dua file
diperiksa manual:

| File | Fungsi | Baris | Manual | `cek.py` |
| --- | --- | --- | --- | --- |
| `src/requests/utils.py` | `super_len` | 160–228 | 69 | 69 |
| `src/requests/models.py` | `prepare_url` | 483–563 | 81 | 81 |

Bukti dan cara hitung: [`tugas-6/README.md`](tugas-6/README.md),
[`tugas-6/hasil_repo.txt`](tugas-6/hasil_repo.txt), dan
[`tugas-6/output/uji.txt`](tugas-6/output/uji.txt).

## Kendala dan cara mengatasinya

- `tree-sitter generate` gagal dengan `Failed to run node` selama Node belum ada
  di PATH; folder Node ditambahkan ke PATH.
- Pointer dari `tree_sitter_filter()` ditolak py-tree-sitter di Windows
  (`OverflowError`), lalu dibungkus `PyCapsule` bernama `tree_sitter.Language`.
- `build/filter.so` dari Linux tidak bisa dibuka di Windows (`WinError 193`),
  jadi parser dibangun ulang sebagai `build/filter.dll`.
- Konfigurasi highlight diletakkan di `%APPDATA%` karena `XDG_CONFIG_HOME` tidak
  dibaca di Windows; `parser-directories` diarahkan ke folder induk proyek.
- Compiler C perlu ditunjuk eksplisit saat tes: `set CC=gcc`.

## Catatan penggunaan AI

Tugas 1–3 saya kerjakan sendiri karena di situ model mental "kode adalah pohon"
terbentuk. AI dipakai di Tugas 4–6 sebagai penulis draf; hasilnya selalu diuji
ulang. Empat kekeliruan yang ditemukan:

- **Tugas 4, operator `in`.** Draf AI menulis daftar nilai sebagai
  `seq('(', $._value, ')')`, sehingga hanya nilai pertama yang masuk dan tes
  kelima gagal. Saya menambahkan rule `value_list` dengan `repeat`; tes lulus.
- **Tugas 5, nama node.** Draf memakai `in_expr` dan `contains_expr`, sedangkan
  grammar menamainya `in_expression` dan `contains_expression`. `tree-sitter
  query` menolak dengan `Invalid node type`; setelah dibetulkan, semua token
  berwarna.
- **Tugas 6, panjang fungsi.** Draf menghitung `end_point[0] - start_point[0]`
  tanpa `+1`, sehingga `super_len` terbaca 68 baris. Hitungan manual baris
  160–228 menghasilkan 69; rumus diperbaiki dan dijalankan ulang.
- **Tugas 6, berkas non-UTF-8.** `errors="replace"` saat mencetak tidak cukup:
  predikat `#match?` sudah lebih dulu gagal mendekode berkas latin-1. Buktinya
  `uji/latin1.py` menghasilkan `UnicodeDecodeError` sebelum perbaikan. Solusinya
  query cadangan `(comment) @c` + `re.search`, ditambah stdout UTF-8. Setelah
  perbaikan, `python cek.py uji` selesai dan tetap melaporkan TODO dari berkas itu.

## Kesimpulan

Tree-sitter memberi struktur yang bisa diperiksa tanpa menjalankan kode: node
bernama dan field cukup untuk membedakan deklarasi, pemanggilan, dan blok, baik
pada kode valid maupun kode yang sedang rusak. Query dan penelusuran pohon saling
melengkapi; query menemukan kandidat, sedangkan penelusuran menangani syarat
struktural yang tidak bisa ditulis sebagai predikat teks. Karena hasilnya
deterministik dan cepat, pemeriksaan seperti Tugas 6 bisa dipasang di alur kerja
sebelum kode masuk ke repositori, sementara AI tetap berguna untuk menulis draf
aturan dan memperbaiki temuan.
