"""main.py - Program utama: menu terminal untuk mengelola silsilah organisasi UIN Suska Riau."""

import sys

from tree.Tree import Tree

# Data contoh = struktur organisasi pada Lembar Aktivitas (Studi Kasus 2).
# Format: (id, nama, jabatan, id_atasan). Atasan selalu ditulis SEBELUM bawahannya.
DATA_CONTOH = [
    ("P001", "Ahmad",   "Rektor", None),
    ("P002", "Budi",    "Senat Universitas", "P001"),
    ("P003", "Citra",   "Wakil Rektor I (Bidang Akademik)", "P001"),
    ("P004", "Dedi",    "Wakil Rektor II (Bidang Administrasi Umum & Keuangan)", "P001"),
    ("P005", "Eka",     "Wakil Rektor III (Bidang Kemahasiswaan & Kerja Sama)", "P001"),
    ("P006", "Fajar",   "Dekan Fakultas Sains dan Teknologi", "P001"),
    ("P007", "Gina",    "Wakil Dekan I (Bidang Akademik & Kelembagaan)", "P006"),
    ("P008", "Hadi",    "Wakil Dekan II (Bidang AUPK)", "P006"),
    ("P009", "Indah",   "Wakil Dekan III (Bidang Kemahasiswaan)", "P006"),
    ("P010", "Joko",    "Ketua Program Studi Teknik Informatika", "P006"),
    ("P011", "Kartika", "Sekretaris Program Studi", "P010"),
    ("P012", "Lukman",  "Kepala Laboratorium Komputer", "P010"),
    ("P013", "Maya",    "Asisten Laboratorium", "P012"),
    ("P014", "Nanda",   "Teknisi Laboratorium", "P012"),
    ("P015", "Oki",     "Koordinator Dosen", "P010"),
    ("P016", "Putri",   "Dosen Pembimbing Akademik", "P015"),
    ("P017", "Rizky",   "Mahasiswa Bimbingan", "P016"),
    ("P018", "Siti",    "Dosen Pengampu Mata Kuliah", "P015"),
]


def isi_data_contoh(tree):
    """Isi Tree dengan DATA_CONTOH. Berhenti dan melapor jika ada yang gagal."""
    for id_pegawai, nama, jabatan, id_atasan in DATA_CONTOH:
        berhasil, pesan = tree.insert_node(id_pegawai, nama, jabatan, id_atasan)
        if not berhasil:
            raise RuntimeError(f"Data contoh tidak valid: {pesan}")


def cetak_urutan(judul, daftar_node):
    """Cetak hasil traversal: daftar bernomor + ringkasan satu baris."""
    print(f"\n=== {judul} ===")
    if not daftar_node:
        print("(Tree kosong)")
        return
    for nomor, node in enumerate(daftar_node, start=1):
        print(f"{nomor:>2}. {node}")
    print("Urutan nama:", " -> ".join(node.nama for node in daftar_node))


def baca_teks(pertanyaan):
    return input(pertanyaan).strip()


# ----------------------------------------------------------------------
# Fungsi untuk setiap menu
# ----------------------------------------------------------------------
def menu_tambah(tree):
    print("\n--- Tambah Pegawai ---")
    id_pegawai = baca_teks("ID pegawai            : ")
    nama = baca_teks("Nama                  : ")
    jabatan = baca_teks("Jabatan               : ")
    id_atasan = baca_teks("ID atasan (kosong=root): ")
    berhasil, pesan = tree.insert_node(id_pegawai, nama, jabatan, id_atasan)
    print(pesan)


def menu_cari(tree):
    print("\n--- Cari Pegawai ---")
    print("1. Berdasarkan ID\n2. Berdasarkan nama\n3. Berdasarkan jabatan")
    pilihan = baca_teks("Pilih (1-3): ")
    pemetaan = {"1": "id", "2": "nama", "3": "jabatan"}
    if pilihan not in pemetaan:
        print("Pilihan tidak valid.")
        return
    kata_kunci = baca_teks("Kata kunci: ")
    if not kata_kunci:
        print("Kata kunci tidak boleh kosong.")
        return
    hasil = tree.search_node(kata_kunci, pemetaan[pilihan])
    if not hasil:
        print(f"Tidak ditemukan pegawai dengan {pemetaan[pilihan]} '{kata_kunci}'.")
        return
    print(f"Ditemukan {len(hasil)} pegawai:")
    for node in hasil:
        print(" -", node)


def menu_detail(tree):
    node = tree.cari_berdasarkan_id(baca_teks("ID pegawai: "))
    if node is None:
        print("Pegawai tidak ditemukan.")
        return
    atasan = node.parent.nama if node.parent else "- (root)"
    print(f"\nID       : {node.id_pegawai}")
    print(f"Nama     : {node.nama}")
    print(f"Jabatan  : {node.jabatan}")
    print(f"Atasan   : {atasan}")
    print(f"Bawahan  : {len(node.children)} orang")


def menu_bawahan(tree):
    id_pegawai = baca_teks("ID pimpinan: ")
    bawahan = tree.daftar_bawahan(id_pegawai)
    if bawahan is None:
        print("Pegawai tidak ditemukan.")
    elif not bawahan:
        print("Pegawai ini tidak memiliki bawahan.")
    else:
        print(f"Bawahan langsung ({len(bawahan)}):")
        for node in bawahan:
            print(" -", node)


def menu_jalur(tree):
    jalur = tree.jalur_dari_root(baca_teks("ID pegawai: "))
    if jalur is None:
        print("Pegawai tidak ditemukan.")
    else:
        print("Jalur:", " -> ".join(node.nama for node in jalur))
        print("Jabatan:", " -> ".join(node.jabatan for node in jalur))


def tampilkan_menu():
    print("\n" + "=" * 50)
    print(" SILSILAH ORGANISASI UIN SULTAN SYARIF KASIM RIAU")
    print("=" * 50)
    print(" 1. Tampilkan struktur organisasi")
    print(" 2. Tambah pegawai")
    print(" 3. Cari pegawai (ID / nama / jabatan)")
    print(" 4. Detail pegawai berdasarkan ID")
    print(" 5. Jumlah seluruh pegawai")
    print(" 6. Bawahan langsung seorang pimpinan")
    print(" 7. Jalur hierarki dari root ke pegawai")
    print(" 8. Traversal Preorder")
    print(" 9. Traversal Inorder (aturan khusus)")
    print("10. Traversal Postorder")
    print("11. Tampilkan ketiga traversal sekaligus")
    print(" 0. Keluar")


def main():
    # Agar karakter garis pohon tampil benar di terminal Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    tree = Tree()
    isi_data_contoh(tree)
    print(f"Data contoh dimuat: {tree.jumlah_pegawai()} pegawai.")

    while True:
        tampilkan_menu()
        try:
            pilihan = baca_teks("Pilih menu: ")
        except (EOFError, KeyboardInterrupt):
            print("\nProgram dihentikan.")
            break

        if pilihan == "0":
            print("Terima kasih.")
            break
        elif pilihan == "1":
            print("\n" + tree.tampilkan_struktur())
        elif pilihan == "2":
            menu_tambah(tree)
        elif pilihan == "3":
            menu_cari(tree)
        elif pilihan == "4":
            menu_detail(tree)
        elif pilihan == "5":
            print(f"Jumlah pegawai: {tree.jumlah_pegawai()}")
        elif pilihan == "6":
            menu_bawahan(tree)
        elif pilihan == "7":
            menu_jalur(tree)
        elif pilihan == "8":
            cetak_urutan("PREORDER", tree.preorder_traversal())
        elif pilihan == "9":
            cetak_urutan("INORDER (aturan khusus)", tree.inorder_traversal())
        elif pilihan == "10":
            cetak_urutan("POSTORDER", tree.postorder_traversal())
        elif pilihan == "11":
            cetak_urutan("PREORDER", tree.preorder_traversal())
            cetak_urutan("INORDER (aturan khusus)", tree.inorder_traversal())
            cetak_urutan("POSTORDER", tree.postorder_traversal())
        else:
            print("Pilihan tidak valid. Masukkan angka 0-11.")


if __name__ == "__main__":
    main()