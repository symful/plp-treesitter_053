# Laporan Praktikum Tree-sitter

Kemal Ardian (251524053), Kelas 2B, D-4 Teknik Informatika, Politeknik Negeri Bandung.
Mata kuliah Programming Language Pragmatics.

Repositori: https://github.com/symful/plp-treesitter_053

## Tugas 1 - Membaca Pohon

`t1.py` mem-parse tiga potongan kode (fungsi, if/else, kelas) dan mencetak pohonnya. Pada potongan fungsi, `def` dan titik dua tampil sebagai node anonim, sedangkan `identifier`, `parameters`, dan `block` bernama. Kode tanpa kolon menghasilkan node `ERROR` dengan `has_error: True`; kondisi `if` yang kosong menghasilkan `MISSING identifier`.

![Tugas 1](dokumentasi/tugas1.png)

## Tugas 2 - Penjelajah Node

`jelajah.py` menelusuri `node.children`, melewati anak anonim, dan memakai `field_name_for_child` sebagai label field. Versi `TreeCursor` menempuh pohon yang sama; hasil keduanya pada `contoh_panjang.py` (115 baris, keluaran 681 baris) dibandingkan dengan `fc` dan tidak ada perbedaan.

![Tugas 2](dokumentasi/tugas2.png)

## Tugas 3 - Query

`rekap_fungsi.py` memasangkan nama fungsi dengan node `parameters` lalu menghitung `named_child_count`. Query lain menemukan 7 pemanggilan `print`, 3 nama modul pada `import` dan `import from`, serta 4 docstring. Semua angka cocok dengan hitungan manual pada `contoh_q.py` dan `contoh_panjang.py`.

![Tugas 3](dokumentasi/tugas3.png)

## Tugas 4 - Grammar DSL Filter

Grammar memuat `comparison`, `in_expression`, `contains_expression`, `and`, `or`, `not`, `parenthesized`, dan tiga jenis nilai. `prec.left` membuat `and` mengikat lebih kuat daripada `or`, sehingga `a = 1 or b = 2 and c = 3` terbaca sebagai `a = 1 or (b = 2 and c = 3)`. Delapan kasus uji lulus. Saat semua `prec` dihapus, `generate` berhenti dengan `Unresolved conflict` pada `'not' _expr 'or'`; `prec` dikembalikan dan tes lulus lagi.

![Tugas 4](dokumentasi/tugas4.png)

## Tugas 5 - Highlight

`highlights.scm` memberi capture untuk keyword, operator, string, number, boolean, nama field, dan tanda kurung. Pada pengayaan, `tugas-4/filter_sql.py` mengubah pohon hasil parse menjadi klausa `WHERE` dengan nilai sebagai parameter, misalnya `status = ? AND (priority > ? OR owner = ?)`.

![Tugas 5](dokumentasi/tugas5.png)

## Tugas 6 - Pemeriksa Kode

`cek.py` melaporkan komentar TODO/FIXME, fungsi lebih dari 30 baris, dan file yang pohonnya error. Pada repo `psf/requests` (37 file) skrip menemukan 7 TODO, sama dengan hasil `find` pada repo yang sama, dan 56 fungsi panjang; `super_len` di `utils.py` baris 160 sampai 228 terhitung 69 baris.

![Tugas 6](dokumentasi/tugas6.png)

## Kendala dan Cara Mengatasinya

- `generate` butuh Node.js; selama node belum ada di PATH, perintah gagal dengan `Failed to run node`. Folder Node ditambahkan ke PATH.
- Pointer dari `tree_sitter_filter()` ditolak py-tree-sitter di Windows (`OverflowError`), lalu dibungkus `PyCapsule` bernama `tree_sitter.Language`.
- `build/filter.so` dari Linux tidak bisa dibuka di Windows (`WinError 193`), jadi parser dibangun ulang sebagai `build/filter.dll`.
- Konfigurasi highlight diletakkan di folder `%APPDATA%` karena `XDG_CONFIG_HOME` tidak dibaca di Windows.

## Catatan Penggunaan AI

Tugas 1 sampai 3 saya kerjakan sendiri karena di situ baru terbentuk kebiasaan melihat pohon sebelum menulis kode. AI mulai dipakai di Tugas 4 sampai 6, hampir selalu sebagai penulis draf yang hasilnya saya uji ulang. Empat kekeliruan berikut yang paling sering muncul dari draf itu.

- Tugas 4, operator `in`. Aturannya harus menerima daftar nilai seperti `status in ("open", "pending", "closed")`. Draf AI menulis daftar itu sebagai `seq('(', $._value, ')')`, jadi hanya nilai pertama yang masuk dan tes kelima di `test/corpus/dasar.txt` gagal. Rule `value_list` dengan `repeat` ditambahkan, tesnya lulus lagi.
- Tugas 5, highlight. Saya minta capture untuk `in` dan `contains`. Draf AI memakai nama node `in_expr` dan `contains_expr`, sedangkan `grammar.js` menamainya `in_expression` dan `contains_expression`. `tree-sitter query` menolak dengan `Invalid node type`, dan itu ketahuan sebelum satu token pun berwarna. Setelah namanya dibetulkan, kedua contoh filter berwarna penuh.
- Tugas 6, fungsi panjang. Draf AI menghitung `end_point[0] - start_point[0]` tanpa menambah satu. `super_len` di `utils.py` jadi terbaca 68 baris, padahal baris 160 sampai 228 berjumlah 69. Selisihnya baru kelihatan setelah dua file di repo requests saya hitung manual, lalu rumusnya diperbaiki dan hasilnya dijalankan ulang.
- Tugas 6, pembacaan berkas. Versi AI memakai `node.text.decode()` polos. Satu file di folder uji memuat byte non-UTF-8 dan skrip berhenti dengan `UnicodeDecodeError` tepat saat mencetak komentar TODO. `errors="replace"` ditambahkan, lalu folder uji dan repo requests dijalankan ulang untuk memastikan tidak ada file yang menggagalkan pemeriksaan.
