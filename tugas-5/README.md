# Tugas 5 - Highlight DSL filter

Tugas ini memberi warna pada token DSL filter. Query-nya ada di `highlights.scm`
pada folder ini, dan salinannya dipasang di proyek grammar sebagai
`../tugas-4/tree-sitter-filter/queries/highlights.scm`, karena CLI tree-sitter
membaca query dari dalam folder proyek.

## Menjalankan

```bat
cd ..\tugas-4\tree-sitter-filter
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
