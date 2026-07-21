from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from ..models import Pinjaman, KonfirmasiPembayaran
from ..services.pinjaman_service import hitung_pinjaman
from ..services.upload_service import save_transfer_proof
from ..utils.validators import validate_confirmation, validate_contact_message
from ..extensions import db
from datetime import datetime

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("public/index.html")


@public_bp.route("/tentang")
def tentang():
    return render_template("public/tentang.html")


@public_bp.route("/simulasi", methods=["GET", "POST"])
def simulasi():
    hasil = None
    if request.method == "POST":
        try:
            jumlah_pinjaman = float(request.form.get("jumlah_pinjaman", 0))
            bunga = float(request.form.get("bunga", 0))
            tenor_minggu = int(request.form.get("tenor_minggu", 0))
            if jumlah_pinjaman <= 0 or bunga < 0 or tenor_minggu <= 0:
                raise ValueError
            hasil = hitung_pinjaman(jumlah_pinjaman, bunga, tenor_minggu)
            hasil.update({
                "jumlah_pinjaman": jumlah_pinjaman,
                "bunga": bunga,
                "tenor_minggu": tenor_minggu,
            })
        except Exception:
            flash("Data simulasi tidak valid.", "danger")
    return render_template("public/simulasi.html", hasil=hasil)


@public_bp.route("/cara-pembayaran")
def cara_pembayaran():
    return render_template("public/cara_pembayaran.html")


@public_bp.route("/konfirmasi-transfer", methods=["GET", "POST"])
def konfirmasi_transfer():
    pinjaman = None
    if request.method == "POST":
        kode_pinjaman = request.form.get("kode_pinjaman", "").strip().upper()
        pinjaman = Pinjaman.query.filter_by(kode_pinjaman=kode_pinjaman).first()
        if not pinjaman:
            flash("Kode pinjaman tidak ditemukan.", "danger")
        else:
            errors = validate_confirmation(request.form)
            file = request.files.get("bukti_transfer")
            if not file or not file.filename:
                errors.append("Bukti transfer wajib diunggah.")
            if errors:
                for err in errors:
                    flash(err, "danger")
            else:
                try:
                    filename = save_transfer_proof(file)
                    konfirmasi = KonfirmasiPembayaran(
                        pinjaman_id=pinjaman.id,
                        tanggal_transfer=datetime.strptime(request.form["tanggal_transfer"], "%Y-%m-%d").date(),
                        nominal=float(request.form["nominal"]),
                        bank_pengirim=request.form["bank_pengirim"].strip(),
                        nama_pengirim=request.form["nama_pengirim"].strip(),
                        bukti_transfer=filename,
                        status="Menunggu",
                        keterangan=request.form.get("keterangan", "").strip() or None,
                    )
                    db.session.add(konfirmasi)
                    db.session.commit()
                    flash("Bukti transfer berhasil dikirim. Status menunggu verifikasi admin.", "success")
                    return redirect(url_for("public.konfirmasi_transfer"))
                except Exception as e:
                    flash(str(e), "danger")
    return render_template("public/konfirmasi_transfer.html", pinjaman=pinjaman)


@public_bp.route("/kontak", methods=["GET", "POST"])
def kontak():
    if request.method == "POST":
        errors = validate_contact_message(request.form)
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            try:
                from ..services.contact_service import create_contact_message
                create_contact_message(request.form)
                flash("Pesan Anda sudah terkirim. Tim kami akan segera menindaklanjuti.", "success")
                return redirect(url_for("public.kontak"))
            except Exception:
                flash("Gagal mengirim pesan. Silakan coba lagi.", "danger")
    return render_template("public/kontak.html")
