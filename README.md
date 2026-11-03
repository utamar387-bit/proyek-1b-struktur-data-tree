# proyek-1b-struktur-data-tree
Implementasi struktur data General Tree menggunakan Python berbasis OOP untuk merepresentasikan hierarki organisasi, dilengkapi operasi Insert, Search, Preorder, Inorder, dan Postorder Traversal.
# PROYEK 1B – STRUKTUR DATA TREE

## Silsilah Organisasi Menggunakan Python Berbasis OOP

### Identitas Mahasiswa

| Keterangan | Informasi |
|---|---|
| Nama | Ridho Utama |
| Program Studi | Teknik Informatika |
| Fakultas | Sains dan Teknologi |
| Universitas | UIN Sultan Syarif Kasim Riau |
| Mata Kuliah | Struktur Data |
| Tahun Akademik | 2025/2026 |

---

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi struktur data Tree menggunakan bahasa pemrograman Python dengan pendekatan Object-Oriented Programming (OOP).

Studi kasus yang digunakan adalah sistem manajemen Silsilah Organisasi di lingkungan Universitas Islam Negeri Sultan Syarif Kasim Riau.

Program ini dirancang untuk merepresentasikan hubungan hierarki antara pimpinan dan bawahan dalam suatu organisasi.

Struktur data yang digunakan adalah **General Tree**, karena setiap node dapat mempunyai lebih dari dua anak.

## 2. Tujuan Proyek

1. Memahami konsep dan penerapan struktur data Tree.
2. Mengimplementasikan struktur Tree menggunakan konsep OOP.
3. Menerapkan operasi penyisipan data (Insert).
4. Menerapkan operasi pencarian data (Search).
5. Mengimplementasikan algoritma Preorder Traversal.
6. Mengimplementasikan algoritma Inorder Traversal.
7. Mengimplementasikan algoritma Postorder Traversal.
8. Menganalisis kompleksitas waktu dan efisiensi algoritma.

## 3. Struktur Data yang Digunakan

Program menggunakan dua kelas utama:

### A. Node

Digunakan untuk menyimpan informasi pegawai, meliputi:
- `id_pegawai`: Identitas pegawai.
- `nama`: Nama pegawai.
- `jabatan`: Jabatan pegawai.
- `children`: Daftar bawahan.

### B. Tree

Digunakan untuk mengelola struktur organisasi, dengan atribut:
- `root`: Node paling atas dalam struktur Tree.

## 4. Fitur Program

| No. | Fitur | Fungsi |
|---|---|---|
| 1 | Insert Node | Menambahkan pegawai di bawah atasan tertentu. |
| 2 | Search Node | Mencari pegawai berdasarkan nama atau jabatan. |
| 3 | Preorder | Mengunjungi node sebelum anak-anaknya. |
| 4 | Inorder | Mengunjungi anak pertama, node, kemudian anak berikutnya sesuai aturan program. |
| 5 | Postorder | Mengunjungi seluruh anak sebelum node induknya. |

## 5. Teknologi yang Digunakan

- Bahasa Pemrograman: Python
- Konsep Pemrograman: Object-Oriented Programming (OOP)
- Struktur Data: General Tree
- Algoritma: Tree Traversal
- Editor: Visual Studio Code

## 6. Cara Menjalankan Program

Pastikan Python sudah terinstal pada komputer.

1. Clone repository:

```bash
git clone https://github.com/USERNAME/proyek-1b-struktur-data-tree.git
```

2. Masuk ke folder proyek:

```bash
cd proyek-1b-struktur-data-tree
```

3. Jalankan program:

```bash
python main.py
```

Ganti `USERNAME` dengan username GitHub pemilik repository.

## 7. Analisis Kompleksitas

Misalkan `n` merupakan jumlah seluruh node dalam Tree.

| Operasi | Kompleksitas Waktu |
|---|---|
| Insert Node | O(n) |
| Search Node | O(n) |
| Preorder Traversal | O(n) |
| Inorder Traversal | O(n) |
| Postorder Traversal | O(n) |

Operasi penyisipan membutuhkan pencarian atasan terlebih dahulu. Oleh karena itu, kompleksitas keseluruhannya adalah O(n) pada kondisi terburuk.

## 8. Kesimpulan

Struktur data General Tree dapat digunakan untuk merepresentasikan hierarki organisasi karena mendukung hubungan antara satu pimpinan dengan banyak bawahan.

Dengan menggunakan Python berbasis OOP, operasi penyisipan, pencarian, dan traversal dapat diimplementasikan secara terstruktur.

Proyek ini memberikan pemahaman mengenai penerapan struktur data Tree dalam menyelesaikan permasalahan hierarki organisasi.

---

**Dibuat oleh Ridho Utama**

Program Studi Teknik Informatika  
Fakultas Sains dan Teknologi  
UIN Sultan Syarif Kasim Riau
