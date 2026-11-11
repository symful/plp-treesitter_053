def hitung_rekap(data):
    total = 0
    jumlah_baris = 0
    jumlah_kosong = 0
    terbesar = 0
    terkecil = None
    for baris in data:
        if baris == "":
            jumlah_kosong = jumlah_kosong + 1
            continue
        nilai = int(baris)
        total = total + nilai
        jumlah_baris = jumlah_baris + 1
        if nilai > terbesar:
            terbesar = nilai
        if terkecil is None:
            terkecil = nilai
        elif nilai < terkecil:
            terkecil = nilai
    rata = 0
    if jumlah_baris > 0:
        rata = total / jumlah_baris
    hasil = {
        "total": total,
        "baris": jumlah_baris,
        "kosong": jumlah_kosong,
        "terbesar": terbesar,
        "terkecil": terkecil,
        "rata": rata,
    }
    return hasil
