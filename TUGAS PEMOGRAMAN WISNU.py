class Buku:
    total_buku_dibuat = 0

    def __init__(self, judul: str, penulis: str, tahun_terbit: int, jumlah_eksemplar: int):
        self.judul = judul
        self.penulis = penulis
        self.__tahun_terbit = 0
        self.__jumlah_eksemplar = 0

        self.tahun_terbit = tahun_terbit
        self.jumlah_eksemplar = jumlah_eksemplar

        Buku.total_buku_dibuat += 1

    @property
    def tahun_terbit(self) -> int:
        return self.__tahun_terbit

    @tahun_terbit.setter
    def tahun_terbit(self, tahun: int):
        if tahun < 1450 or tahun > 2026:
            raise ValueError("Tahun terbit tidak valid (harus antara 1450 - 2026).")
        self.__tahun_terbit = tahun

    @property
    def jumlah_eksemplar(self) -> int:
        return self.__jumlah_eksemplar

    @jumlah_eksemplar.setter
    def jumlah_eksemplar(self, jumlah: int):
        if jumlah < 0:
            raise ValueError("Jumlah eksemplar tidak boleh negatif.")
        self.__jumlah_eksemplar = jumlah

    def pinjam_eksemplar(self) -> bool:
        if self.__jumlah_eksemplar > 0:
            self.__jumlah_eksemplar -= 1
            return True
        return False

    def kembalikan_eksemplar(self):
        self.__jumlah_eksemplar += 1

    @classmethod
    def info_total_buku(cls) -> str:
        return f"Total objek buku yang terdaftar: {cls.total_buku_dibuat}"

    @staticmethod
    def cek_kode_valid(kode: str) -> bool:
        return kode.startswith("BK-") and len(kode) >= 5 and kode[3:].isdigit()


class Perpustakaan:
    def __init__(self, nama_perpustakaan: str):
        self.nama_perpustakaan = nama_perpustakaan

        self.koleksi = {}
        self.pinjaman_aktif = []

    def tambah_buku(self, kode: str, buku: Buku):
        if not Buku.cek_kode_valid(kode):
            print(f"[GAGAL] Kode '{kode}' tidak valid. Gunakan format seperti 'BK-001'.")
            return
        if kode in self.koleksi:
            print(f"[GAGAL] Kode '{kode}' sudah digunakan.")
            return
        self.koleksi[kode] = buku
        print(f"[OK] Buku '{buku.judul}' ({kode}) berhasil ditambahkan.")

    def pinjam_buku(self, nama_peminjam: str, kode: str):
        if kode not in self.koleksi:
            print(f"[GAGAL] Buku dengan kode '{kode}' tidak ditemukan.")
            return

        buku = self.koleksi[kode]
        if buku.pinjam_eksemplar():
            self.pinjaman_aktif.append({"peminjam": nama_peminjam, "kode": kode, "judul": buku.judul})
            print(f"[BERHASIL] {nama_peminjam} meminjam '{buku.judul}'. Sisa stok: {buku.jumlah_eksemplar}")
        else:
            print(f"[GAGAL] Stok '{buku.judul}' sedang kosong.")

    def kembalikan_buku(self, nama_peminjam: str, kode: str):
        for i, data in enumerate(self.pinjaman_aktif):
            if data["peminjam"] == nama_peminjam and data["kode"] == kode:
                self.koleksi[kode].kembalikan_eksemplar()
                self.pinjaman_aktif.pop(i)
                print(f"[KEMBALI] '{data['judul']}' dikembalikan oleh {nama_peminjam}. Stok sekarang: {self.koleksi[kode].jumlah_eksemplar}")
                return
        print(f"[GAGAL] Data peminjaman untuk {nama_peminjam} dengan kode '{kode}' tidak ditemukan.")

    def tampilkan_koleksi(self):
        print(f"\n=== KOLEKSI {self.nama_perpustakaan.upper()} ===")
        for kode, buku in self.koleksi.items():
            print(
                f"[{kode}] {buku.judul} - {buku.penulis} ({buku.tahun_terbit}) | "
                f"Stok: {buku.jumlah_eksemplar}"
            )
        print()



if __name__ == "__main__":

    buku_1 = Buku("Pemrograman Python Dasar", "Budi Raharjo", 2023, 3)
    buku_2 = Buku("Struktur Data & Algoritma", "Rinaldi Munir", 2021, 2)

    perpus = Perpustakaan("Perpustakaan Kampus")
    perpus.tambah_buku("BK-101", buku_1)
    perpus.tambah_buku("BK-102", buku_2)
    perpus.tambah_buku("SALAH", buku_1)  

    buku_1.jumlah_eksemplar = 5
    print(f"Stok terbaru '{buku_1.judul}': {buku_1.jumlah_eksemplar}")

    perpus.pinjam_buku("Andi", "BK-101")
    perpus.pinjam_buku("Siti", "BK-102")
    perpus.tampilkan_koleksi()

    perpus.kembalikan_buku("Andi", "BK-101")
    perpus.tampilkan_koleksi()

    print(Buku.info_total_buku())