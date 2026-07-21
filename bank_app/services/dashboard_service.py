from datetime import date

from sqlalchemy import func

from ..models import Nasabah, Pinjaman, KonfirmasiPembayaran, RiwayatPembayaran


def get_stats():
    total_nasabah = Nasabah.query.count()
    total_pinjaman = Pinjaman.query.count()
    pinjaman_aktif = Pinjaman.query.filter_by(status="Aktif").count()
    pinjaman_lunas = Pinjaman.query.filter_by(status="Lunas").count()
    konfirmasi_menunggu = KonfirmasiPembayaran.query.filter_by(status="Menunggu").count()
    total_dana = float(sum((p.jumlah_pinjaman or 0) for p in Pinjaman.query.all()))
    total_pembayaran = float(sum((r.jumlah_bayar or 0) for r in RiwayatPembayaran.query.all()))
    total_konfirmasi = KonfirmasiPembayaran.query.count()
    return {
        "total_nasabah": total_nasabah,
        "total_pinjaman": total_pinjaman,
        "pinjaman_aktif": pinjaman_aktif,
        "pinjaman_lunas": pinjaman_lunas,
        "konfirmasi_menunggu": konfirmasi_menunggu,
        "total_dana": total_dana,
        "total_pembayaran": total_pembayaran,
        "total_konfirmasi": total_konfirmasi,
    }


def get_chart_data():
    current_year = date.today().year

    monthly_values = []
    for month in range(1, 13):
        total = 0.0
        for loan in Pinjaman.query.all():
            if loan.tanggal_pinjam and loan.tanggal_pinjam.year == current_year and loan.tanggal_pinjam.month == month:
                total += float(loan.jumlah_pinjaman or 0)
        monthly_values.append(total)

    weekly_values = []
    for week in range(1, 13):
        total = 0.0
        for payment in RiwayatPembayaran.query.filter_by(minggu_ke=week).all():
            total += float(payment.jumlah_bayar or 0)
        weekly_values.append(total)

    return {
        "monthly_labels": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
        "monthly_values": monthly_values,
        "weekly_labels": [f"M{w}" for w in range(1, 13)],
        "weekly_values": weekly_values,
    }


def get_recent_activity(limit=8):
    loans = Pinjaman.query.order_by(Pinjaman.id.desc()).limit(limit).all()
    confirmations = KonfirmasiPembayaran.query.order_by(KonfirmasiPembayaran.id.desc()).limit(limit).all()
    return loans, confirmations
