from flask import Blueprint, render_template
from ..models import RiwayatPembayaran, Pinjaman
from ..utils.helpers import login_required

pembayaran_bp = Blueprint("pembayaran", __name__, url_prefix="/dashboard/pembayaran")


@pembayaran_bp.route("/")
@login_required
def list_pembayaran():
    data = RiwayatPembayaran.query.order_by(RiwayatPembayaran.id.desc()).all()
    return render_template("dashboard/pembayaran.html", pembayaran_list=data)


@pembayaran_bp.route("/loan/<int:pinjaman_id>")
@login_required
def pembayaran_by_loan(pinjaman_id):
    loan = Pinjaman.query.get_or_404(pinjaman_id)
    return render_template("dashboard/pembayaran.html", pembayaran_list=loan.riwayat, loan=loan)
