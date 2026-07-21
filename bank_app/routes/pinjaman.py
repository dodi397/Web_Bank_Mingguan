from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import Pinjaman, Nasabah
from ..extensions import db
from ..utils.helpers import login_required
from ..utils.validators import validate_pinjaman
from ..services.pinjaman_service import create_pinjaman, recalculate_pinjaman

pinjaman_bp = Blueprint("pinjaman", __name__, url_prefix="/dashboard/pinjaman")


@pinjaman_bp.route("/")
@login_required
def list_pinjaman():
    data = Pinjaman.query.order_by(Pinjaman.id.desc()).all()
    return render_template("dashboard/pinjaman.html", pinjaman_list=data)


@pinjaman_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_pinjaman():
    nasabah_list = Nasabah.query.order_by(Nasabah.nama.asc()).all()
    if request.method == "POST":
        errors = validate_pinjaman(request.form)
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            try:
                create_pinjaman(
                    request.form["nasabah_id"],
                    request.form["jumlah_pinjaman"],
                    request.form["bunga"],
                    request.form["tenor_minggu"],
                )
                flash("Data pinjaman berhasil ditambahkan.", "success")
                return redirect(url_for("pinjaman.list_pinjaman"))
            except Exception as e:
                db.session.rollback()
                flash("Gagal menambahkan pinjaman.", "danger")
    return render_template("dashboard/tambah_pinjaman.html", nasabah_list=nasabah_list)


@pinjaman_bp.route("/edit/<int:pinjaman_id>", methods=["GET", "POST"])
@login_required
def edit_pinjaman(pinjaman_id):
    loan = Pinjaman.query.get_or_404(pinjaman_id)
    nasabah_list = Nasabah.query.order_by(Nasabah.nama.asc()).all()
    if request.method == "POST":
        errors = validate_pinjaman(request.form)
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            try:
                loan.nasabah_id = int(request.form["nasabah_id"])
                recalculate_pinjaman(
                    loan,
                    request.form["jumlah_pinjaman"],
                    request.form["bunga"],
                    request.form["tenor_minggu"],
                )
                flash("Data pinjaman berhasil diperbarui.", "success")
                return redirect(url_for("pinjaman.list_pinjaman"))
            except Exception:
                db.session.rollback()
                flash("Gagal memperbarui pinjaman.", "danger")
    return render_template("dashboard/edit_pinjaman.html", pinjaman=loan, nasabah_list=nasabah_list)


@pinjaman_bp.route("/delete/<int:pinjaman_id>", methods=["POST"])
@login_required
def delete_pinjaman(pinjaman_id):
    loan = Pinjaman.query.get_or_404(pinjaman_id)
    db.session.delete(loan)
    db.session.commit()
    flash("Data pinjaman berhasil dihapus.", "success")
    return redirect(url_for("pinjaman.list_pinjaman"))
