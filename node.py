"""node.py - Kelas Node: menyimpan data SATU pegawai dan hubungannya."""


class Node:
    """Satu simpul (pegawai) dalam General Tree.

    Atribut:
        id_pegawai : ID unik pegawai, contoh "P001"
        nama       : nama pegawai
        jabatan    : jabatan pegawai
        children   : daftar bawahan langsung (urutan = urutan penambahan)
        parent     : atasan langsung (None jika node ini adalah root)
    """

    def __init__(self, id_pegawai, nama, jabatan):
        self.id_pegawai = id_pegawai
        self.nama = nama
        self.jabatan = jabatan
        self.children = []   # awalnya belum punya bawahan
        self.parent = None   # diisi saat node dipasang ke atasan

    def tambah_anak(self, node_anak):
        """Pasang node_anak sebagai bawahan node ini (dua arah: parent & children)."""
        node_anak.parent = self
        self.children.append(node_anak)

    def adalah_daun(self):
        """True jika node tidak punya bawahan."""
        return len(self.children) == 0

    def __str__(self):
        return f"{self.id_pegawai} {self.nama} ({self.jabatan})"