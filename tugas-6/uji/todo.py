import os


def baca(path):
    with open(path) as f:
        return f.read()


def main():
    # TODO: tambahkan penanganan berkas kosong
    isi = baca("data.txt")
    print(isi)
    # FIXME: belum menutup berkas kalau terjadi error
    os.remove("data.txt")


main()
