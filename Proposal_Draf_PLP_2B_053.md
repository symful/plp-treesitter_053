# Draf Proposal Proyek PLP

## Linter Aturan Tim untuk API Express Berbasis tree-sitter

Kemal Ardian (251524053) - Kelas 2B - D-4 Teknik Informatika, Politeknik Negeri Bandung

**1. Judul.** Linter aturan tim untuk API Express berbasis tree-sitter.

**2. Masalah.** Tim backend yang mengerjakan API dengan Express punya aturan internal yang mudah dilanggar: `console.log` tertinggal di kode produksi, handler rute tanpa `try/catch` sehingga error async tidak tertangani, dan query SQL yang dibentuk dengan penggabungan string. Review manual tidak konsisten karena setiap reviewer memeriksa hal yang berbeda, sedangkan `grep` sering salah karena mencocokkan teks di dalam komentar atau string. Yang dirugikan adalah reviewer, developer yang mendapat komentar berulang, dan tim QA yang menemukan bug di produksi.

**3. Kenapa tidak cukup dengan AI saja.** Meminta AI memeriksa setiap pull request memberi hasil yang berbeda-beda, tidak bisa dipakai sebagai syarat merge yang objektif, dan biayanya tumbuh seiring jumlah file. Linter berbasis tree-sitter membaca struktur kode, jadi hasilnya sama setiap kali dijalankan, cepat, dan bisa dipasang di CI sebagai gerbang sebelum merge. AI tetap dipakai untuk menulis aturan dan memperbaiki temuan, bukan sebagai satu-satunya pemeriksa.

**4. Bahasa dan framework target.** JavaScript dan TypeScript pada Express, dengan grammar `tree-sitter-javascript` 0.25.0 dan `tree-sitter-typescript` dari PyPI.

**5. Contoh kode.**

Harus terdeteksi:

```js
app.get('/users', async (req, res) => {
  console.log('debug');
  const rows = await db.query("SELECT * FROM users WHERE id = " + req.params.id);
  res.json(rows);
});
```

Tidak boleh terdeteksi: teks `console.log` di dalam komentar atau string; `console.error` di blok `catch`; dan `console.log` di dalam `if (process.env.NODE_ENV !== 'production')` (difilter dengan pemeriksaan konteks, bukan regex).

**6. Rancangan query.**

Aturan `console.log` memakai `call_expression`, bukan `call`:

```scheme
(call_expression
  function: (member_expression
    object: (identifier) @obj
    property: (property_identifier) @prop)
  (#eq? @obj "console")
  (#eq? @prop "log"))
```

Aturan `try/catch` menangkap bentuk handler yang relevan, lalu struktur pohonnya diperiksa di Python. Query tidak memakai `#not-match?` karena predikat itu memeriksa teks, bukan keberadaan node:

```scheme
(call_expression
  function: (member_expression
    property: (property_identifier) @method)
  arguments: (arguments
    [
      (arrow_function body: (statement_block) @body)
      (function_expression body: (statement_block) @body)
    ] @handler)
  (#match? @method "^(get|post|put|patch|delete|all)$"))
```

Untuk setiap `@handler`, skrip menelusuri `@body` dan melaporkan handler yang tidak memiliki turunan `try_statement`. Penelusuran berhenti di batas fungsi bersarang agar `try` di dalam callback tidak dianggap melindungi handler. Kedua query sudah diuji dengan `tree-sitter-javascript` 0.25.0: query `console.log` menemukan satu pemanggilan, dan query handler menemukan dua handler dengan status `try=False` dan `try=True`.

**7. Bentuk output.** Laporan terminal `file:baris: aturan: pesan`, kode keluar 1 bila ada temuan, dan opsi `--json` agar hasilnya bisa dibaca GitHub Actions. Ringkasan akhir menyebut jumlah temuan per aturan.

**8. Cara evaluasi.** Repo uji: `expressjs/express` tag `4.21.2` (commit `1faf228935aa0a13111f92c28ee795be64ce3f0f`) dan `gothinkster/node-express-realworld-example-app` (commit `30b68e1e881462b2f4164ea09ab4c4f5699c7b0b`). Sebanyak 20 temuan dari kedua repo diperiksa manual untuk mengukur presisi; setiap aturan juga diuji dengan contoh negatif yang seharusnya lolos. Hasilnya dicatat dalam tabel `temuan | benar | salah | alasan`.

**9. Rencana kerja dan risiko.**

| Minggu | Kegiatan |
| --- | --- |
| 1 | Menyiapkan parser, query dasar, dan kerangka CLI |
| 2 | Aturan `console.log` dan filter konteks `NODE_ENV` |
| 3 | Aturan `try/catch` dan aturan SQL string concat |
| 4 | Uji pada dua repo, cek manual 20 temuan, perbaiki presisi |
| 5 | Keluaran JSON, integrasi CI sederhana, laporan dan demo |

Risiko utama: query terlalu longgar pada kode TypeScript dan banyak false positive dari `console.log` yang memang disengaja. Mitigasinya adalah uji negatif per aturan dan pemeriksaan manual sebelum aturan diaktifkan sebagai gerbang CI.
