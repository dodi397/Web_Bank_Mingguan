# Bank Mingguan

Aplikasi Bank Mingguan merupakan sistem berbasis Python Flask yang digunakan untuk mengelola data nasabah, pinjaman mingguan, pembayaran angsuran, konfirmasi transfer, serta laporan administrasi dalam satu aplikasi yang terintegrasi.

Aplikasi ini memiliki halaman publik untuk pengunjung serta dashboard admin untuk mengelola seluruh data.

---

## Fitur

### Halaman Publik
- Beranda
- Tentang
- Simulasi Pinjaman
- Cara Pembayaran
- Konfirmasi Transfer
- Kontak

### Dashboard Admin
- Login Admin
- Dashboard Statistik
- CRUD Nasabah
- CRUD Pinjaman
- Data Pembayaran
- Konfirmasi Transfer
- Pengaturan Pembayaran
- Pengaturan Kontak
- Pesan Kontak
- Laporan
- Detail Pembayaran
- Detail Pesan Kontak

---

## Struktur Project
Project menggunakan arsitektur modular sehingga setiap bagian aplikasi dipisahkan berdasarkan tanggung jawabnya agar lebih mudah dikembangkan dan dipelihara.

---

## Teknologi

- Python 3
- Flask
- Flask-SQLAlchemy
- HTML5
- CSS3
- JavaScript
- SQLite

---

## Instalasi

Clone repository

```bash
git clone https://github.com/username/bank-mingguan.git
```

Masuk ke folder project

```bash
cd bank-mingguan
```

Install dependency

```bash
pip install -r requirements.txt
```

Jalankan aplikasi

```bash
python app.py
```

Buka browser

```
http://127.0.0.1:5000
```

---

## Requirements

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Werkzeug==3.1.8
```

---

## Desain

Aplikasi menggunakan tampilan modern dengan tema hijau yang responsif.

Fitur antarmuka meliputi:

- Responsive Layout
- Sidebar Dashboard
- Statistik Dashboard
- CSS
- Form Validasi
- Upload Bukti Transfer
- Dashboard Admin
- Public Website

---

## Modul Aplikasi

### Public
- Beranda
- Tentang
- Simulasi Pinjaman
- Cara Pembayaran
- Konfirmasi Transfer
- Kontak

### Admin
- Dashboard
- Nasabah
- Pinjaman
- Pembayaran
- Konfirmasi
- Laporan
- Pengaturan Pembayaran
- Pengaturan Kontak
- Pesan Kontak

---

## Penyimpanan

Aplikasi menyimpan data menggunakan SQLite melalui SQLAlchemy.

Folder upload digunakan untuk menyimpan:

```
bank_app/static/uploads/bukti_transfer/
```

---

## Pengembangan

Struktur aplikasi dibuat secara modular dengan pemisahan:

- Routes
- Services
- Templates
- Static Assets
- Utilities
- Database Models

Pendekatan ini memudahkan proses pengembangan, debugging, serta penambahan fitur baru.

---

## Lisensi

Project ini dibuat untuk keperluan pembelajaran, pengembangan, dan implementasi aplikasi berbasis Flask.