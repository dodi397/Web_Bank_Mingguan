from datetime import datetime, date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import Nasabah
from ..extensions import db
from ..utils.helpers import login_required
from ..utils.validators import validate_nasabah

nasabah_bp = Blueprint("nasabah", __name__, url_prefix="/dashboard/nasabah")


@nasabah_bp.route("/")
@login_required
def list_nasabah():
    data = Nasabah.query.order_by(Nasabah.id.desc()).all()
    return render_template("dashboard/nasabah.html", nasabah_list=data)


@nasabah_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_nasabah():
    if request.method == "POST":
        errors = validate_nasabah(request.form)
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            try:
                tanggal_daftar_raw = request.form.get("tanggal_daftar")
                tanggal_daftar = datetime.strptime(tanggal_daftar_raw, "%Y-%m-%d").date() if tanggal_daftar_raw else date.today()
                nasabah = Nasabah(
                    nama=request.form["nama"].strip(),
                    nik=request.form["nik"].strip(),
                    alamat=request.form["alamat"].strip(),
                    no_hp=request.form["no_hp"].strip(),
                    pekerjaan=request.form["pekerjaan"].strip(),
                    tanggal_daftar=tanggal_daftar,
                )
                db.session.add(nasabah)
                db.session.commit()
                flash("Data nasabah berhasil ditambahkan.", "success")
                return redirect(url_for("nasabah.list_nasabah"))
            except Exception:
                db.session.rollback()
                flash("Gagal menambahkan nasabah. Pastikan NIK belum digunakan.", "danger")
    return render_template("dashboard/tambah_nasabah.html")


@nasabah_bp.route("/edit/<int:nasabah_id>", methods=["GET", "POST"])
@login_required
def edit_nasabah(nasabah_id):
    nasabah = Nasabah.query.get_or_404(nasabah_id)
    if request.method == "POST":
        errors = validate_nasabah(request.form)
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            try:
                nasabah.nama = request.form["nama"].strip()
                nasabah.nik = request.form["nik"].strip()
                nasabah.alamat = request.form["alamat"].strip()
                nasabah.no_hp = request.form["no_hp"].strip()
                nasabah.pekerjaan = request.form["pekerjaan"].strip()
                db.session.commit()
                flash("Data nasabah berhasil diperbarui.", "success")
                return redirect(url_for("nasabah.list_nasabah"))
            except Exception:
                db.session.rollback()
                flash("Gagal memperbarui nasabah. Pastikan NIK belum digunakan.", "danger")
    return render_template("dashboard/edit_nasabah.html", nasabah=nasabah)


@nasabah_bp.route("/delete/<int:nasabah_id>", methods=["POST"])
@login_required
def delete_nasabah(nasabah_id):
    nasabah = Nasabah.query.get_or_404(nasabah_id)
    db.session.delete(nasabah)
    db.session.commit()
    flash("Data nasabah berhasil dihapus.", "success")
    return redirect(url_for("nasabah.list_nasabah"))
