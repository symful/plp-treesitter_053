class Akun:
    def __init__(self, saldo):
        self.saldo = saldo

    def tarik(self, jumlah):
        self.saldo = self.saldo - jumlah
        return self.saldo
