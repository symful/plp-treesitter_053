# Tugas 5 - Highlight DSL filter

Tugas ini memberi warna pada token DSL filter. Query-nya ada di `highlights.scm`
pada folder ini, dan salinannya dipasang di proyek grammar sebagai
`../tugas-4/tree-sitter-filter/queries/highlights.scm`, karena CLI tree-sitter
membaca query dari dalam folder proyek.

## Setup CLI sekali saja

`tree-sitter highlight` membutuhkan konfigurasi global yang menunjuk ke folder
**induk** proyek grammar, bukan ke folder `tree-sitter-filter/` itu sendiri.
Langkah ini yang membuat perintah highlight bisa dijalankan dari folder mana pun.

1. Buat konfigurasi:

   ```bat
   tree-sitter init-config
   ```

   Perintah ini mencetak lokasi berkas konfigurasi. Di Windows biasanya:

   ```text
   C:\Users\<nama>\AppData\Roaming\tree-sitter\config.json
   ```

2. Buka berkas itu, lalu isi `parser-directories` dengan folder induk proyek.
   Untuk repositori ini, folder induknya adalah `tugas-4`:

   ```json
   {
     "parser-directories": [
       "C:\\path\\ke\\plp-treesitter\\tugas-4"
     ]
   }
   ```

   Jangan menulis `...\tugas-4\tree-sitter-filter`; CLI akan mencari
   `tree-sitter-filter/` di dalam setiap direktori yang terdaftar.

3. Periksa `tugas-4/tree-sitter-filter/tree-sitter.json`: `file-types` harus
   memuat `"filter"` dan `highlights` harus menunjuk ke
   `queries/highlights.scm`.

4. Uji dari folder lain, bukan dari dalam proyek:

   ```bat
   cd %USERPROFILE%
   tree-sitter parse C:\path\ke\plp-treesitter\tugas-4\tree-sitter-filter\contoh.filter
   ```

   Kalau perintah ini berhasil, `parser-directories` sudah benar. Kalau gagal,
   highlight juga tidak akan menemukan grammar.

## Menjalankan highlight

```bat
cd tugas-4\tree-sitter-filter
tree-sitter highlight contoh.filter
tree-sitter highlight contoh2.filter
```

Kalau `highlights.scm` diubah, salin dulu ke proyek:

```bat
copy ..\..\tugas-5\highlights.scm queries\highlights.scm
```

## Capture yang dipakai

| Node | Capture | Warna |
| --- | --- | --- |
| `and`, `or`, `not`, `in`, `contains` | `@keyword` | kata kunci |
| `=`, `!=`, `>`, `<`, `>=`, `<=` | `@operator` | operator |
| `string` | `@string` | teks |
| `number` | `@number` | angka |
| `boolean` | `@constant.builtin` | konstanta |
| `identifier` pada `field:` | `@property` | nama kolom |
| `(`, `)`, `,` | `@punctuation` | tanda baca |

## Bukti tekstual

Karena keluaran berwarna sulit dibaca sebagai teks, bukti yang disimpan adalah
hasil query capture (nama capture dan posisi) di `output/t5_query_contoh.txt`
dan `output/t5_query_contoh2.txt`, serta keluaran `filter_sql.py` di
`output/t5_sql.txt`. Perintah `tree-sitter highlight` tetap dijalankan untuk
memastikan tidak ada error `Invalid node type`; warnanya diperiksa langsung di
terminal saat demo.
