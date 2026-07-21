from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


def today_date():
    return date.today()


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(120), nullable=False)

    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)


class PaymentSetting(db.Model):
    __tablename__ = "payment_settings"

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(80), nullable=False, default="BCA")
    account_name = db.Column(db.String(120), nullable=False, default="A/N BANK MINGGUAN")
    account_number = db.Column(db.String(40), nullable=False, default="1234567890")
    qris_label = db.Column(db.String(120), nullable=False, default="BANK MINGGUAN QRIS")
    qris_image = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False, default="Jl. Merdeka No. 123, Jakarta")
    contact_phone = db.Column(db.String(40), nullable=False, default="0812-3456-7890")
    contact_email = db.Column(db.String(120), nullable=False, default="info@bankmingguan.id")
    contact_note = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    no_hp = db.Column(db.String(30), nullable=True)
    pesan = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Baru")
    dibaca_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Nasabah(db.Model):
    __tablename__ = "nasabah"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    nik = db.Column(db.String(32), unique=True, nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    no_hp = db.Column(db.String(30), nullable=False)
    pekerjaan = db.Column(db.String(120), nullable=False)
    tanggal_daftar = db.Column(db.Date, default=today_date, nullable=False)

    pinjaman = db.relationship(
        "Pinjaman",
        backref="nasabah",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Pinjaman(db.Model):
    __tablename__ = "pinjaman"

    id = db.Column(db.Integer, primary_key=True)
    nasabah_id = db.Column(db.Integer, db.ForeignKey("nasabah.id"), nullable=False)
    kode_pinjaman = db.Column(db.String(40), unique=True, nullable=False)
    jumlah_pinjaman = db.Column(db.Float, nullable=False)
    bunga = db.Column(db.Float, nullable=False)
    tenor_minggu = db.Column(db.Integer, nullable=False)
    angsuran_per_minggu = db.Column(db.Float, nullable=False)
    total_tagihan = db.Column(db.Float, nullable=False)
    sisa_tagihan = db.Column(db.Float, nullable=False)
    tanggal_pinjam = db.Column(db.Date, default=today_date, nullable=False)
    status = db.Column(db.String(20), default="Aktif", nullable=False)

    konfirmasi = db.relationship(
        "KonfirmasiPembayaran",
        backref="pinjaman",
        lazy=True,
        cascade="all, delete-orphan",
    )
    riwayat = db.relationship(
        "RiwayatPembayaran",
        backref="pinjaman",
        lazy=True,
        cascade="all, delete-orphan",
    )


class KonfirmasiPembayaran(db.Model):
    __tablename__ = "konfirmasi_pembayaran"

    id = db.Column(db.Integer, primary_key=True)
    pinjaman_id = db.Column(db.Integer, db.ForeignKey("pinjaman.id"), nullable=False)
    tanggal_transfer = db.Column(db.Date, nullable=False)
    nominal = db.Column(db.Float, nullable=False)
    bank_pengirim = db.Column(db.String(120), nullable=False)
    nama_pengirim = db.Column(db.String(120), nullable=False)
    bukti_transfer = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="Menunggu", nullable=False)
    keterangan = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class RiwayatPembayaran(db.Model):
    __tablename__ = "riwayat_pembayaran"

    id = db.Column(db.Integer, primary_key=True)
    pinjaman_id = db.Column(db.Integer, db.ForeignKey("pinjaman.id"), nullable=False)
    konfirmasi_id = db.Column(db.Integer, db.ForeignKey("konfirmasi_pembayaran.id"), nullable=True)
    minggu_ke = db.Column(db.Integer, nullable=False)
    tanggal_bayar = db.Column(db.Date, default=today_date, nullable=False)
    jumlah_bayar = db.Column(db.Float, nullable=False)
    sisa_tagihan = db.Column(db.Float, nullable=False)
    metode = db.Column(db.String(50), default="Transfer", nullable=False)

    konfirmasi = db.relationship("KonfirmasiPembayaran", foreign_keys=[konfirmasi_id], lazy=True)
