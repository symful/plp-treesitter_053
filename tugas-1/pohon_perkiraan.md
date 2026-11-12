# Tugas 1 - Pohon perkiraan dan perbandingannya dengan hasil parser

Berkas ini melengkapi `t1.py` dan keluaran di `output/`. Isinya menjawab dua hal
yang diminta rubrik: pohon yang diperkirakan lebih dulu untuk setiap potongan,
lalu perbandingannya dengan pohon yang benar-benar dihasilkan parser, serta
perbedaan `children` dan `named_children`.

Catatan kejujuran: pada pengerjaan pertama, pohon perkiraan tidak diarsipkan.
Perkiraan di bawah ditulis ulang saat bukti ini disusun, baru setelah itu
`t1.py` dijalankan ulang dan hasilnya dibandingkan. Jadi bagian ini adalah
pengulangan proses yang benar-benar dilakukan sekarang, bukan klaim bahwa
arsip perkiraan sudah ada sejak awal.

## Cara mengulang

```bat
cd tugas-1
python t1.py potongan1.py
python t1.py potongan2.py
python t1.py potongan3.py
python t1.py potongan1_rusak.py
python t1.py potongan2_rusak.py
python t1.py potongan3_rusak.py
```

Keluaran lengkap ada di `output/t1_*.txt`.

## 1. Fungsi - `potongan1.py`

Kode:

```python
def sapa(nama):
    pesan = "Halo, " + nama
    return pesan
```

Perkiraan sebelum dijalankan:

```text
(module
  (function_definition
    name: (identifier)
    parameters: (parameters (identifier))
    body: (block
      (expression_statement
        (assignment
          left: (identifier)
          right: (binary_operator
            left: (string)
            right: (identifier))))
      (return_statement (identifier)))))
```

Hasil parser (diringkas dari `output/t1_potongan1.txt`):

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

Perbandingan:

| Bagian | Perkiraan | Hasil parser | Status |
| --- | --- | --- | --- |
| `module` -> `function_definition` | ada | ada | sesuai |
| field `name`, `parameters`, `body` | ada | ada | sesuai |
| `assignment` dan `binary_operator` | ada | ada | sesuai |
| isi node `string` | hanya `(string)` | `(string_start) (string_content) (string_end)` | **berbeda** |
| `def` dan `:` | tidak digambar | node anonim di dalam `function_definition` | **berbeda** |

Perbedaan pertama muncul karena grammar Python memecah string menjadi penanda
awal, isi, dan penanda akhir. Perbedaan kedua adalah node anonim: `def` dan `:`
tidak tampil di S-expression karena bukan node bernama, tetapi tetap ada di
`children`. Itulah sebabnya pohon yang "terlihat" di output tidak sama dengan
daftar `children` mentah.

## 2. If/else - `potongan2.py`

Kode:

```python
nilai = 78
if nilai >= 75:
    status = "lulus"
else:
    status = "tidak lulus"
```

Perkiraan sebelum dijalankan:

```text
(module
  (expression_statement (assignment left: (identifier) right: (integer)))
  (if_statement
    condition: (comparison_operator (identifier) (integer))
    consequence: (block
      (expression_statement (assignment left: (identifier) right: (string))))
    alternative: (else_clause
      body: (block
        (expression_statement (assignment left: (identifier) right: (string)))))))
```

Hasil parser (diringkas dari `output/t1_potongan2.txt`):

```text
(module
  (expression_statement (assignment left: (identifier) right: (integer)))
  (if_statement
    condition: (comparison_operator (identifier) (integer))
    consequence: (block (expression_statement (assignment left: (identifier)
      right: (string (string_start) (string_content) (string_end)))))
    alternative: (else_clause body: (block (expression_statement
      (assignment left: (identifier)
        right: (string (string_start) (string_content) (string_end))))))))
```

Perbandingan:

| Bagian | Perkiraan | Hasil parser | Status |
| --- | --- | --- | --- |
| `if_statement` dan field `condition` | ada | ada | sesuai |
| `else_clause` dengan field `body` | ada | ada | sesuai |
| urutan `consequence` lalu `alternative` | ada | ada | sesuai |
| isi node `string` | hanya `(string)` | `string_start`, `string_content`, `string_end` | **berbeda** |
| `if`, `:`, dan `else` | tidak digambar | node anonim | **berbeda** |

## 3. Kelas - `potongan3.py`

Kode:

```python
class Akun:
    def __init__(self, saldo):
        self.saldo = saldo

    def tarik(self, jumlah):
        self.saldo = self.saldo - jumlah
        return self.saldo
```

Perkiraan sebelum dijalankan:

```text
(module
  (class_definition
    name: (identifier)
    body: (block
      (function_definition
        name: (identifier)
        parameters: (parameters (identifier) (identifier))
        body: (block
          (expression_statement
            (assignment
              left: (attribute (identifier) (identifier))
              right: (identifier)))))
      (function_definition
        name: (identifier)
        parameters: (parameters (identifier) (identifier))
        body: (block
          (expression_statement
            (assignment
              left: (attribute (identifier) (identifier))
              right: (binary_operator
                left: (attribute (identifier) (identifier))
                right: (identifier))))
          (return_statement (attribute (identifier) (identifier))))))))
```

Hasil parser (diringkas dari `output/t1_potongan3.txt`):

```text
(module (class_definition name: (identifier)
  body: (block
    (function_definition name: (identifier)
      parameters: (parameters (identifier) (identifier))
      body: (block (expression_statement
        (assignment
          left: (attribute object: (identifier) attribute: (identifier))
          right: (identifier)))))
    (function_definition name: (identifier)
      parameters: (parameters (identifier) (identifier))
      body: (block
        (expression_statement (assignment
          left: (attribute object: (identifier) attribute: (identifier))
          right: (binary_operator
            left: (attribute object: (identifier) attribute: (identifier))
            right: (identifier))))
        (return_statement
          (attribute object: (identifier) attribute: (identifier))))))))
```

Perbandingan:

| Bagian | Perkiraan | Hasil parser | Status |
| --- | --- | --- | --- |
| `class_definition` dan method di dalam `block` | ada | ada | sesuai |
| dua `function_definition` | ada | ada | sesuai |
| `attribute` untuk `self.saldo` | ada | ada | sesuai |
| label field pada `attribute` | tidak ditulis | `object:` dan `attribute:` | **berbeda** |
| `class` dan `:` | tidak digambar | node anonim | **berbeda** |

## 4. Kode rusak - `potongan1_rusak.py`

Kode (titik dua setelah `def sapa(nama)` dihapus):

```python
def sapa(nama)
    pesan = "Halo, " + nama
    return pesan
```

Perkiraan: parser akan menandai baris `def` sebagai `ERROR`, lalu tetap membaca
dua baris berikutnya sebagai pernyataan biasa di dalam `module`.

Hasil parser (`output/t1_potongan1_rusak.txt`):

```text
(module (ERROR (identifier) (parameters (identifier)) (identifier)
  (expression_statement (binary_operator left: (string ...) right: (identifier)))
  (return_statement (identifier))))
has_error: True
```

Perbandingan: perkiraan bahwa ada `ERROR` benar, tetapi jangkauannya lebih
besar dari dugaan. Seluruh fungsi menjadi satu node `ERROR`; `def` dan `=`
tetap ada sebagai anak anonim, sedangkan `identifier`, `parameters`, dan
`return_statement` menjadi anak bernama.

## 5. Kode rusak - `potongan2_rusak.py`

Kode (tanda tutup kurung dihapus):

```python
print("halo"
```

Perkiraan: akan muncul `MISSING ")"` di dalam `argument_list`.

Hasil parser (`output/t1_potongan2_rusak.txt`):

```text
(module (ERROR (string (string_start) (string_content) (string_end))))
has_error: True
```

Perbandingan: perkiraan **salah**. Parser tidak memakai `MISSING ")"` di sini,
melainkan membungkus `print`, `(`, dan string ke dalam satu node `ERROR`.
Node `print` dan `(` menjadi anak anonim, string menjadi anak bernama.

## 6. Kode rusak - `potongan3_rusak.py`

Kode (kondisi `if` dikosongkan):

```python
nilai = 78
status = "lulus" if else "tidak lulus"
```

Perkiraan: `conditional_expression` akan terbentuk dengan satu node
`MISSING identifier` sebagai kondisi.

Hasil parser (`output/t1_potongan3_rusak.txt`):

```text
(module
  (expression_statement (assignment left: (identifier) right: (integer)))
  (expression_statement
    (assignment left: (identifier)
      right: (conditional_expression
        (string (string_start) (string_content) (string_end))
        (MISSING identifier)
        (string (string_start) (string_content) (string_end))))))
has_error: True
```

Perbandingan: sesuai. Parser menyisipkan `MISSING identifier` tepat di posisi
kondisi yang hilang, dan `has_error` bernilai `True`.

## 7. `children` dan `named_children`

`t1.py` sekarang mencetak kedua daftar untuk node yang punya anak anonim.
Contoh dari `potongan1.py`:

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

Perbedaannya:

- `children` berisi **semua** anak, termasuk token anonim seperti `def` dan `:`.
  Panjangnya 5 dan indeksnya dipakai oleh `field_name_for_child(i)`.
- `named_children` hanya berisi anak bernama, yaitu `identifier`, `parameters`,
  dan `block`. Panjangnya 3 dan indeksnya **tidak** sama dengan indeks di
  `children`.

Kesalahan yang mudah terjadi: memakai indeks dari `named_children` untuk
memanggil `field_name_for_child()`. Pada contoh di atas, `named_children[1]`
adalah `parameters`, sedangkan `children[1]` adalah `identifier` dengan field
`name`. Kalau indeks tertukar, label field yang muncul akan bergeser. Karena
itu `jelajah.py` di Tugas 2 memakai `enumerate(node.children)` lalu menyaring
`is_named`, bukan mengindeks `named_children`.

Contoh lain dari `potongan2.py`: `if_statement` punya 5 `children` tetapi hanya
3 `named_children`; yang hilang dari daftar bernama adalah `if` dan `:`.
