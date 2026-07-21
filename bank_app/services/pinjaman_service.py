from datetime import date

from sqlalchemy import func

from ..extensions import db
from ..models import Pinjaman


def generate_kode_pinjaman():
    today = date.today().strftime("%Y%m%d")
    last_id = db.session.query(func.coalesce(func.max(Pinjaman.id), 0)).scalar() or 0
    next_number = int(last_id) + 1
    return f"PJ{today}{next_number:04d}"


def hitung_pinjaman(jumlah_pinjaman: float, bunga: float, tenor_minggu: int):
    jumlah_pinjaman = float(jumlah_pinjaman)
    bunga = float(bunga)
    tenor_minggu = int(tenor_minggu)
    total_bunga = jumlah_pinjaman * (bunga / 100.0) * tenor_minggu
    total_tagihan = jumlah_pinjaman + total_bunga
    angsuran = total_tagihan / tenor_minggu
    return {
        "total_bunga": total_bunga,
        "total_tagihan": total_tagihan,
        "angsuran_per_minggu": angsuran,
    }


def create_pinjaman(nasabah_id, jumlah_pinjaman, bunga, tenor_minggu):
    calc = hitung_pinjaman(jumlah_pinjaman, bunga, tenor_minggu)
    loan = Pinjaman(
        nasabah_id=int(nasabah_id),
        kode_pinjaman=generate_kode_pinjaman(),
        jumlah_pinjaman=float(jumlah_pinjaman),
        bunga=float(bunga),
        tenor_minggu=int(tenor_minggu),
        angsuran_per_minggu=calc["angsuran_per_minggu"],
        total_tagihan=calc["total_tagihan"],
        sisa_tagihan=calc["total_tagihan"],
        status="Aktif",
    )
    db.session.add(loan)
    db.session.commit()
    return loan


def recalculate_pinjaman(loan, jumlah_pinjaman, bunga, tenor_minggu):
    calc = hitung_pinjaman(jumlah_pinjaman, bunga, tenor_minggu)
    loan.jumlah_pinjaman = float(jumlah_pinjaman)
    loan.bunga = float(bunga)
    loan.tenor_minggu = int(tenor_minggu)
    loan.angsuran_per_minggu = calc["angsuran_per_minggu"]
    loan.total_tagihan = calc["total_tagihan"]
    if loan.sisa_tagihan > loan.total_tagihan:
        loan.sisa_tagihan = loan.total_tagihan
    if loan.sisa_tagihan <= 0:
        loan.status = "Lunas"
    elif loan.status == "Lunas":
        loan.status = "Aktif"
    db.session.commit()
    return loan
