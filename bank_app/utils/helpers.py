import os
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from .formatter import rupiah, format_date, badge_class, percent


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


def unique_filename(original_name: str, prefix: str = "file") -> str:
    safe = secure_filename(original_name)
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    name, ext = os.path.splitext(safe)
    return f"{prefix}_{stamp}{ext.lower()}"


def make_flash_message(message, category="success"):
    return message, category


def loan_progress(loan) -> float:
    try:
        if not loan.total_tagihan:
            return 0
        return max(0, min(100, ((loan.total_tagihan - loan.sisa_tagihan) / loan.total_tagihan) * 100))
    except Exception:
        return 0
