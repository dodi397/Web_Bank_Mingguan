from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import KonfirmasiPembayaran
from ..extensions import db
from ..utils.helpers import login_required
from ..services.pembayaran_service import apply_confirmation, reject_confirmation

konfirmasi_bp = Blueprint("konfirmasi", __name__, url_prefix="/dashboard/konfirmasi")


@konfirmasi_bp.route("/")
@login_required
def list_konfirmasi():
    data = KonfirmasiPembayaran.query.order_by(KonfirmasiPembayaran.id.desc()).all()
    return render_template("dashboard/konfirmasi.html", konfirmasi_list=data)


@konfirmasi_bp.route("/accept/<int:konfirmasi_id>", methods=["POST"])
@login_required
def accept_konfirmasi(konfirmasi_id):
    konfirmasi = KonfirmasiPembayaran.query.get_or_404(konfirmasi_id)
    if konfirmasi.status != "Menunggu":
        flash("Status sudah diproses.", "warning")
    else:
        apply_confirmation(konfirmasi)
        flash("Konfirmasi diterima dan pembayaran tercatat.", "success")
    return redirect(url_for("konfirmasi.list_konfirmasi"))


@konfirmasi_bp.route("/reject/<int:konfirmasi_id>", methods=["POST"])
@login_required
def reject_konfirmasi_route(konfirmasi_id):
    konfirmasi = KonfirmasiPembayaran.query.get_or_404(konfirmasi_id)
    if konfirmasi.status != "Menunggu":
        flash("Status sudah diproses.", "warning")
    else:
        alasan = request.form.get("keterangan", "").strip() or "Data transfer tidak sesuai."
        reject_confirmation(konfirmasi, alasan)
        flash("Konfirmasi ditolak.", "info")
    return redirect(url_for("konfirmasi.list_konfirmasi"))


@konfirmasi_bp.route("/detail/<int:konfirmasi_id>")
@login_required
def detail_konfirmasi(konfirmasi_id):
    konfirmasi = KonfirmasiPembayaran.query.get_or_404(konfirmasi_id)
    return render_template("dashboard/detail_pembayaran.html", konfirmasi=konfirmasi)
