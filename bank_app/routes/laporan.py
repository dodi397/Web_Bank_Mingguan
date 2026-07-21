import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, request, Response
from sqlalchemy import func
from ..models import Pinjaman, RiwayatPembayaran, KonfirmasiPembayaran
from ..utils.helpers import login_required
from ..utils.formatter import rupiah, format_date

laporan_bp = Blueprint("laporan", __name__, url_prefix="/dashboard/laporan")


@laporan_bp.route("/")
@login_required
def laporan_home():
    periode = request.args.get("periode", "bulanan")
    total_pinjaman = Pinjaman.query.with_entities(func.coalesce(func.sum(Pinjaman.jumlah_pinjaman), 0)).scalar() or 0
    total_pembayaran = RiwayatPembayaran.query.with_entities(func.coalesce(func.sum(RiwayatPembayaran.jumlah_bayar), 0)).scalar() or 0
    total_konfirmasi = KonfirmasiPembayaran.query.count()
    return render_template(
        "dashboard/laporan.html",
        periode=periode,
        total_pinjaman=total_pinjaman,
        total_pembayaran=total_pembayaran,
        total_konfirmasi=total_konfirmasi,
    )


@laporan_bp.route("/export.csv")
@login_required
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Kode Pinjaman", "Nasabah", "Jumlah Pinjaman", "Sisa Tagihan", "Status"])
    for loan in Pinjaman.query.order_by(Pinjaman.id.desc()).all():
        writer.writerow([
            loan.kode_pinjaman,
            loan.nasabah.nama,
            loan.jumlah_pinjaman,
            loan.sisa_tagihan,
            loan.status,
        ])
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=laporan_pinjaman.csv"
    return response
