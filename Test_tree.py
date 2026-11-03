"""test_tree.py - Unit test (unittest bawaan Python).

Jalankan:  python -m unittest test_tree -v

Urutan yang diharapkan (EXPECTED_*) ditulis TANGAN dari gambar struktur
organisasi di Lembar Aktivitas, bukan disalin dari keluaran program,
sehingga pengujian benar-benar membandingkan kode dengan hitungan manual.
"""

import unittest

from main import isi_data_contoh
from tree.Tree import Tree

EXPECTED_PREORDER = ["P001", "P002", "P003", "P004", "P005", "P006", "P007",
                     "P008", "P009", "P010", "P011", "P012", "P013", "P014",
                     "P015", "P016", "P017", "P018"]
EXPECTED_INORDER = ["P002", "P001", "P003", "P004", "P005", "P007", "P006",
                    "P008", "P009", "P011", "P010", "P013", "P012", "P014",
                    "P017", "P016", "P015", "P018"]
EXPECTED_POSTORDER = ["P002", "P003", "P004", "P005", "P007", "P008", "P009",
                      "P011", "P013", "P014", "P012", "P017", "P016", "P018",
                      "P015", "P010", "P006", "P001"]


def ambil_id(daftar_node):
    return [node.id_pegawai for node in daftar_node]


def buat_tree_kecil():
    """Tree kecil 8 pegawai (contoh rancangan awal) untuk uji urutan."""
    t = Tree()
    data = [("P001", "Ahmad", "Rektor", None),
            ("P002", "Budi", "Dekan Fakultas Sains dan Teknologi", "P001"),
            ("P003", "Citra", "Dekan Fakultas Tarbiyah", "P001"),
            ("P004", "Dedi", "Ketua Prodi Teknik Informatika", "P002"),
            ("P005", "Eka", "Ketua Prodi Sistem Informasi", "P002"),
            ("P006", "Fajar", "Ketua Prodi Pendidikan Agama Islam", "P003"),
            ("P007", "Gina", "Dosen Teknik Informatika", "P004"),
            ("P008", "Hadi", "Dosen Sistem Informasi", "P005")]
    for d in data:
        assert t.insert_node(*d)[0]
    return t


class TestInsert(unittest.TestCase):
    def test_01_tree_kosong(self):
        t = Tree()
        self.assertTrue(t.kosong())
        self.assertEqual(t.jumlah_pegawai(), 0)
        self.assertEqual(t.preorder_traversal(), [])
        self.assertEqual(t.inorder_traversal(), [])
        self.assertEqual(t.postorder_traversal(), [])

    def test_02_tambah_root(self):
        t = Tree()
        ok, _ = t.insert_node("P001", "Ahmad", "Rektor")
        self.assertTrue(ok)
        self.assertEqual(t.root.nama, "Ahmad")
        self.assertIsNone(t.root.parent)

    def test_03_tambah_di_bawah_atasan_benar(self):
        t = Tree()
        t.insert_node("P001", "Ahmad", "Rektor")
        ok, _ = t.insert_node("P002", "Budi", "Dekan", "P001")
        self.assertTrue(ok)
        self.assertEqual(ambil_id(t.root.children), ["P002"])
        self.assertIs(t.cari_berdasarkan_id("P002").parent, t.root)

    def test_04_id_duplikat_ditolak(self):
        t = buat_tree_kecil()
        ok, pesan = t.insert_node("P002", "Orang Lain", "Dosen", "P001")
        self.assertFalse(ok)
        self.assertIn("sudah digunakan", pesan)
        self.assertEqual(t.jumlah_pegawai(), 8)       # Tree tidak berubah
        self.assertEqual(t.cari_berdasarkan_id("P002").nama, "Budi")

    def test_05_atasan_tidak_ditemukan(self):
        t = buat_tree_kecil()
        ok, pesan = t.insert_node("P099", "Zaki", "Dosen", "P404")
        self.assertFalse(ok)
        self.assertIn("tidak ditemukan", pesan)
        self.assertEqual(t.jumlah_pegawai(), 8)
        self.assertIsNone(t.cari_berdasarkan_id("P099"))

    def test_data_kosong_ditolak(self):
        t = buat_tree_kecil()
        self.assertFalse(t.insert_node("P090", "", "Dosen", "P001")[0])
        self.assertFalse(t.insert_node("P090", "Zaki", "   ", "P001")[0])
        self.assertFalse(t.insert_node("", "Zaki", "Dosen", "P001")[0])
        self.assertEqual(t.jumlah_pegawai(), 8)

    def test_root_kedua_dan_atasan_pada_tree_kosong_ditolak(self):
        t = Tree()
        self.assertFalse(t.insert_node("P001", "Ahmad", "Rektor", "P000")[0])
        self.assertTrue(t.kosong())
        t.insert_node("P001", "Ahmad", "Rektor")
        self.assertFalse(t.insert_node("P002", "Budi", "Dekan")[0])
        self.assertEqual(t.jumlah_pegawai(), 1)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.t = Tree()
        isi_data_contoh(self.t)

    def test_06_cari_id(self):
        hasil = self.t.search_node("P016", "id")
        self.assertEqual(ambil_id(hasil), ["P016"])       # node level dalam
        self.assertEqual(ambil_id(self.t.search_node("p016", "id")), ["P016"])

    def test_07_cari_nama_tanpa_beda_huruf(self):
        self.assertEqual(ambil_id(self.t.search_node("RIZKY", "nama")), ["P017"])
        self.assertEqual(ambil_id(self.t.search_node("kartika", "nama")), ["P011"])

    def test_08_cari_jabatan_banyak_hasil(self):
        hasil = self.t.search_node("wakil rektor", "jabatan")
        self.assertEqual(ambil_id(hasil), ["P003", "P004", "P005"])
        hasil = self.t.search_node("DOSEN", "jabatan")
        self.assertEqual(ambil_id(hasil), ["P015", "P016", "P018"])

    def test_09_data_tidak_ada(self):
        self.assertEqual(self.t.search_node("P999", "id"), [])
        self.assertEqual(self.t.search_node("Zzz", "nama"), [])
        self.assertEqual(self.t.search_node("Bendahara", "jabatan"), [])
        self.assertEqual(self.t.search_node("", "nama"), [])
        self.assertIsNone(self.t.cari_berdasarkan_id("P999"))


class TestTraversal(unittest.TestCase):
    def test_10_preorder(self):
        t = Tree(); isi_data_contoh(t)
        self.assertEqual(ambil_id(t.preorder_traversal()), EXPECTED_PREORDER)

    def test_11_inorder_aturan_khusus(self):
        t = Tree(); isi_data_contoh(t)
        self.assertEqual(ambil_id(t.inorder_traversal()), EXPECTED_INORDER)

    def test_12_postorder(self):
        t = Tree(); isi_data_contoh(t)
        self.assertEqual(ambil_id(t.postorder_traversal()), EXPECTED_POSTORDER)

    def test_13_urutan_sesuai_struktur_tree(self):
        t = Tree(); isi_data_contoh(t)
        pre = ambil_id(t.preorder_traversal())
        post = ambil_id(t.postorder_traversal())
        ino = ambil_id(t.inorder_traversal())
        # Semua pegawai dikunjungi tepat sekali oleh ketiga traversal
        semua = sorted(EXPECTED_PREORDER)
        self.assertEqual(sorted(pre), semua)
        self.assertEqual(sorted(ino), semua)
        self.assertEqual(sorted(post), semua)
        self.assertEqual(len(pre), t.jumlah_pegawai())
        # Root pertama di preorder, terakhir di postorder
        self.assertEqual((pre[0], post[-1]), ("P001", "P001"))
        # Setiap atasan muncul sebelum bawahannya (preorder) dan sesudahnya (postorder)
        for node in t.preorder_traversal():
            if node.parent:
                self.assertLess(pre.index(node.parent.id_pegawai), pre.index(node.id_pegawai))
                self.assertGreater(post.index(node.parent.id_pegawai), post.index(node.id_pegawai))

    def test_traversal_tree_kecil(self):
        t = buat_tree_kecil()
        self.assertEqual(ambil_id(t.preorder_traversal()),
                         ["P001", "P002", "P004", "P007", "P005", "P008", "P003", "P006"])
        self.assertEqual(ambil_id(t.inorder_traversal()),
                         ["P007", "P004", "P002", "P008", "P005", "P001", "P006", "P003"])
        self.assertEqual(ambil_id(t.postorder_traversal()),
                         ["P007", "P004", "P008", "P005", "P002", "P006", "P003", "P001"])


class TestFiturTambahan(unittest.TestCase):
    def setUp(self):
        self.t = Tree()
        isi_data_contoh(self.t)

    def test_jumlah_dan_level(self):
        self.assertEqual(self.t.jumlah_pegawai(), 18)
        self.assertEqual(self.t.jumlah_level(), 6)

    def test_jalur_dari_root(self):
        self.assertEqual(ambil_id(self.t.jalur_dari_root("P017")),
                         ["P001", "P006", "P010", "P015", "P016", "P017"])
        self.assertIsNone(self.t.jalur_dari_root("P999"))

    def test_daftar_bawahan(self):
        self.assertEqual(ambil_id(self.t.daftar_bawahan("P010")), ["P011", "P012", "P015"])
        self.assertEqual(self.t.daftar_bawahan("P017"), [])
        self.assertIsNone(self.t.daftar_bawahan("P999"))

    def test_parent_dan_children_konsisten(self):
        for node in self.t.preorder_traversal():
            for anak in node.children:
                self.assertIs(anak.parent, node)


if __name__ == "__main__":
    unittest.main()