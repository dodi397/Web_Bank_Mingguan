from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..utils.helpers import login_required
from ..services.payment_setting_service import get_payment_setting, update_payment_setting


pengaturan_bp = Blueprint("pengaturan", __name__, url_prefix="/dashboard/pengaturan-pembayaran")


@pengaturan_bp.route("/", methods=["GET", "POST"])
@login_required
def pengaturan_pembayaran():
    setting = get_payment_setting()

    if request.method == "POST":
        try:
            update_payment_setting(setting, request.form, request.files.get("qris_image"))
            flash("Pengaturan pembayaran berhasil diperbarui.", "success")
            return redirect(url_for("pengaturan.pengaturan_pembayaran"))
        except Exception as exc:
            flash(str(exc), "danger")

    return render_template("dashboard/pengaturan_pembayaran.html", setting=setting)
