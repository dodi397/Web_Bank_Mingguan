from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.nasabah import nasabah_bp
from .routes.pinjaman import pinjaman_bp
from .routes.pembayaran import pembayaran_bp
from .routes.konfirmasi import konfirmasi_bp
from .routes.laporan import laporan_bp
from .routes.pengaturan import pengaturan_bp
from .routes.pengaturan_kontak import pengaturan_kontak_bp
from .routes.pesan_kontak import pesan_kontak_bp

ALL_BLUEPRINTS = [
    public_bp,
    auth_bp,
    dashboard_bp,
    nasabah_bp,
    pinjaman_bp,
    pembayaran_bp,
    konfirmasi_bp,
    laporan_bp,
    pengaturan_bp,
    pengaturan_kontak_bp,
    pesan_kontak_bp,
]
