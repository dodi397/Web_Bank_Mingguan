from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..services.auth_service import authenticate_admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/dashboard/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("dashboard.dashboard_home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        admin = authenticate_admin(username, password)
        if admin:
            session["admin_id"] = admin.id
            session["admin_nama"] = admin.nama
            flash("Login berhasil.", "success")
            return redirect(url_for("dashboard.dashboard_home"))
        flash("Username atau password salah.", "danger")
    return render_template("dashboard/login.html")


@auth_bp.route("/dashboard/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("public.index"))
