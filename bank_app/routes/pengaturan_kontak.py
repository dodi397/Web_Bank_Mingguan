from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..services.site_setting_service import get_site_setting, update_site_setting
from ..utils.helpers import login_required

pengaturan_kontak_bp = Blueprint("pengaturan_kontak", __name__, url_prefix="/dashboard/pengaturan-kontak")


@pengaturan_kontak_bp.route("/", methods=["GET", "POST"])
@login_required
def pengaturan_kontak():
    setting = get_site_setting()

    if request.method == "POST":
        try:
            update_site_setting(setting, request.form)
            flash("Pengaturan kontak berhasil diperbarui.", "success")
            return redirect(url_for("pengaturan_kontak.pengaturan_kontak"))
        except Exception as exc:
            flash(str(exc), "danger")

    return render_template("dashboard/pengaturan_kontak.html", setting=setting)
