from datetime import date
from ..extensions import db
from ..models import RiwayatPembayaran, KonfirmasiPembayaran, Pinjaman


def next_week_number(loan: Pinjaman) -> int:
    latest = RiwayatPembayaran.query.filter_by(pinjaman_id=loan.id).order_by(RiwayatPembayaran.minggu_ke.desc()).first()
    return (latest.minggu_ke + 1) if latest else 1


def apply_confirmation(confirmation: KonfirmasiPembayaran):
    loan = confirmation.pinjaman
    paid = min(float(confirmation.nominal), float(loan.sisa_tagihan))
    new_sisa = max(0.0, float(loan.sisa_tagihan) - paid)
    riwayat = RiwayatPembayaran(
        pinjaman_id=loan.id,
        konfirmasi_id=confirmation.id,
        minggu_ke=next_week_number(loan),
        tanggal_bayar=date.today(),
        jumlah_bayar=paid,
        sisa_tagihan=new_sisa,
        metode="Transfer",
    )
    loan.sisa_tagihan = new_sisa
    if new_sisa <= 0:
        loan.status = "Lunas"
    confirmation.status = "Diterima"
    db.session.add(riwayat)
    db.session.commit()
    return riwayat


def reject_confirmation(confirmation: KonfirmasiPembayaran, reason: str = "Data transfer tidak sesuai."):
    confirmation.status = "Ditolak"
    confirmation.keterangan = reason
    db.session.commit()
    return confirmation
