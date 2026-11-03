"""tree.py - Kelas Tree: mengelola seluruh hierarki organisasi (General Tree)."""

from models.node import Node


class Tree:
    """General Tree: satu node boleh punya banyak anak.

    Selain root, Tree menyimpan dictionary `_indeks_id` (ID -> Node) agar
    pengecekan ID ganda dan pencarian atasan cepat (rata-rata O(1)).
    Dictionary ini selalu diperbarui bersama Tree di insert_node().
    """

    def __init__(self):
        self.root = None
        self._indeks_id = {}

    # ------------------------------------------------------------------
    # Fungsi bantu
    # ------------------------------------------------------------------
    @staticmethod
    def _bersihkan(teks):
        """Hapus spasi di tepi; kembalikan "" jika bukan teks."""
        return teks.strip() if isinstance(teks, str) else ""

    def kosong(self):
        return self.root is None

    # ------------------------------------------------------------------
    # 1. INSERT
    # ------------------------------------------------------------------
    def insert_node(self, id_pegawai, nama, jabatan, id_atasan=None):
        """Tambah pegawai baru. Mengembalikan (berhasil, pesan).

        Cara kerja:
          1. Validasi dulu: ID, nama, jabatan tidak boleh kosong.
          2. Tolak jika ID sudah dipakai (cek di dictionary).
          3. Jika id_atasan kosong -> pegawai ini harus jadi ROOT
             (hanya boleh bila Tree masih kosong).
          4. Jika id_atasan diisi -> cari atasan di dictionary. Tidak ketemu
             -> tolak.
          5. Baru setelah semua lolos, Node dibuat dan dipasang sebagai
             anak terakhir atasan. Node baru selalu jadi DAUN, jadi tidak
             mungkin membentuk siklus. Jika ada yang gagal, Tree tidak
             berubah sama sekali.
        """
        id_pegawai = self._bersihkan(id_pegawai).upper()  # "p001" == "P001"
        nama = self._bersihkan(nama)
        jabatan = self._bersihkan(jabatan)
        id_atasan = self._bersihkan(id_atasan).upper()

        # Langkah 1 - validasi data wajib
        if not id_pegawai or not nama or not jabatan:
            return False, "Gagal: ID, nama, dan jabatan wajib diisi."

        # Langkah 2 - ID harus unik
        if id_pegawai in self._indeks_id:
            return False, f"Gagal: ID {id_pegawai} sudah digunakan."

        # Langkah 3 - kasus root
        if not id_atasan:
            if not self.kosong():
                return False, ("Gagal: Tree sudah punya root. "
                               "Sebutkan ID atasan untuk pegawai ini.")
            node_baru = Node(id_pegawai, nama, jabatan)
            self.root = node_baru
            self._indeks_id[id_pegawai] = node_baru
            return True, f"Berhasil: {node_baru} ditambahkan sebagai ROOT."

        # Langkah 4 - cari atasan
        atasan = self._indeks_id.get(id_atasan)
        if atasan is None:
            return False, f"Gagal: atasan dengan ID {id_atasan} tidak ditemukan."

        # Langkah 5 - semua lolos, baru ubah Tree
        node_baru = Node(id_pegawai, nama, jabatan)
        atasan.tambah_anak(node_baru)
        self._indeks_id[id_pegawai] = node_baru
        return True, f"Berhasil: {node_baru} ditambahkan di bawah {atasan.nama}."

    # ------------------------------------------------------------------
    # 2. SEARCH
    # ------------------------------------------------------------------
    def cari_berdasarkan_id(self, id_pegawai):
        """Cari satu pegawai lewat ID. Mengembalikan Node atau None."""
        return self._indeks_id.get(self._bersihkan(id_pegawai).upper())

    def search_node(self, kata_kunci, berdasarkan="nama"):
        """Cari pegawai. Selalu mengembalikan LIST (kosong = tidak ada).

        berdasarkan = "id"      -> paling banyak 1 hasil (ID unik)
        berdasarkan = "nama"    -> SEMUA node yang namanya mengandung kata_kunci
        berdasarkan = "jabatan" -> SEMUA node yang jabatannya mengandung kata_kunci

        Pencocokan nama/jabatan: tidak membedakan huruf besar/kecil dan
        cukup mengandung kata kunci ("dosen" cocok dengan "Dosen Pengampu
        Mata Kuliah"). Penelusuran memakai preorder ke seluruh Tree, jadi
        hasil berurutan dari atas ke bawah.
        """
        kata_kunci = self._bersihkan(kata_kunci)
        if not kata_kunci:
            return []

        if berdasarkan == "id":
            node = self.cari_berdasarkan_id(kata_kunci)
            return [node] if node else []

        if berdasarkan not in ("nama", "jabatan"):
            raise ValueError("berdasarkan harus 'id', 'nama', atau 'jabatan'")

        kata = kata_kunci.lower()
        hasil = []
        for node in self.preorder_traversal():      # telusuri semua node
            teks = node.nama if berdasarkan == "nama" else node.jabatan
            if kata in teks.lower():
                hasil.append(node)
        return hasil

    # ------------------------------------------------------------------
    # 3-5. TRAVERSAL (mengembalikan list Node; pencetakan dilakukan main.py)
    # ------------------------------------------------------------------
    def preorder_traversal(self):
        """Preorder: node saat ini -> semua anak (kiri ke kanan)."""
        hasil = []
        self._preorder(self.root, hasil)
        return hasil

    def _preorder(self, node, hasil):
        if node is None:
            return
        hasil.append(node)                       # 1. kunjungi node
        for anak in node.children:               # 2. lalu semua anak
            self._preorder(anak, hasil)

    def inorder_traversal(self):
        """Inorder ATURAN KHUSUS proyek ini (bukan definisi standar):
        anak pertama -> node saat ini -> anak kedua dan seterusnya.

        Pada General Tree, node bisa punya >2 anak sehingga tidak ada satu
        "posisi tengah" yang baku seperti di Binary Tree. Karena itu aturan
        ini adalah kesepakatan untuk tugas ini. Node tanpa anak: hanya dirinya.
        """
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node is None:
            return
        if node.children:
            self._inorder(node.children[0], hasil)   # 1. anak pertama
        hasil.append(node)                           # 2. node saat ini
        for anak in node.children[1:]:               # 3. anak kedua dst.
            self._inorder(anak, hasil)

    def postorder_traversal(self):
        """Postorder: semua anak (kiri ke kanan) -> node saat ini."""
        hasil = []
        self._postorder(self.root, hasil)
        return hasil

    def _postorder(self, node, hasil):
        if node is None:
            return
        for anak in node.children:                   # 1. semua anak dulu
            self._postorder(anak, hasil)
        hasil.append(node)                           # 2. baru node ini

    # ------------------------------------------------------------------
    # Fitur tambahan
    # ------------------------------------------------------------------
    def jumlah_pegawai(self):
        return len(self._indeks_id)

    def jumlah_level(self):
        """Jumlah level (root saja = 1, Tree kosong = 0). Dipakai sebagai h."""
        return self._level(self.root)

    def _level(self, node):
        if node is None:
            return 0
        if node.adalah_daun():
            return 1
        return 1 + max(self._level(anak) for anak in node.children)

    def daftar_bawahan(self, id_pegawai):
        """Bawahan langsung. None jika ID tidak ada, [] jika tidak punya bawahan."""
        node = self.cari_berdasarkan_id(id_pegawai)
        return None if node is None else list(node.children)

    def jalur_dari_root(self, id_pegawai):
        """Jalur root -> pegawai, naik lewat parent lalu dibalik. O(h)."""
        node = self.cari_berdasarkan_id(id_pegawai)
        if node is None:
            return None
        jalur = []
        while node is not None:
            jalur.append(node)
            node = node.parent
        jalur.reverse()
        return jalur

    def tampilkan_struktur(self):
        """Kembalikan teks struktur organisasi dengan indentasi per level."""
        if self.kosong():
            return "(Tree kosong)"
        baris = [str(self.root)]
        self._gambar(self.root, "", baris)
        return "\n".join(baris)

    def _gambar(self, node, awalan, baris):
        for i, anak in enumerate(node.children):
            terakhir = (i == len(node.children) - 1)
            baris.append(awalan + ("└── " if terakhir else "├── ") + str(anak))
            self._gambar(anak, awalan + ("    " if terakhir else "│   "), baris)