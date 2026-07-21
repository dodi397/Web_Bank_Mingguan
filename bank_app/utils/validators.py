from datetime import date


def _required(form, field):
    value = (form.get(field) or "").strip()
    return value


def validate_nasabah(form):
    errors = []
    for field, label in [
        ("nama", "Nama"),
        ("nik", "NIK"),
        ("alamat", "Alamat"),
        ("no_hp", "No HP"),
        ("pekerjaan", "Pekerjaan"),
    ]:
        if not _required(form, field):
            errors.append(f"{label} wajib diisi.")
    if form.get("nik") and not form["nik"].isdigit():
        errors.append("NIK harus berisi angka.")
    return errors


def validate_pinjaman(form):
    errors = []
    nasabah_id = _required(form, "nasabah_id")
    jumlah_pinjaman = _required(form, "jumlah_pinjaman")
    bunga = _required(form, "bunga")
    tenor_minggu = _required(form, "tenor_minggu")
    if not nasabah_id:
        errors.append("Nasabah wajib dipilih.")
    for value, label in [(jumlah_pinjaman, "Jumlah pinjaman"), (bunga, "Bunga"), (tenor_minggu, "Tenor minggu")]:
        if not value:
            errors.append(f"{label} wajib diisi.")
    try:
        if float(jumlah_pinjaman) <= 0:
            errors.append("Jumlah pinjaman harus lebih dari 0.")
    except Exception:
        errors.append("Jumlah pinjaman tidak valid.")
    try:
        if float(bunga) < 0:
            errors.append("Bunga tidak boleh negatif.")
    except Exception:
        errors.append("Bunga tidak valid.")
    try:
        if int(tenor_minggu) <= 0:
            errors.append("Tenor minggu harus lebih dari 0.")
    except Exception:
        errors.append("Tenor minggu tidak valid.")
    return errors


def validate_confirmation(form):
    errors = []
    required_fields = {
        "kode_pinjaman": "Kode pinjaman",
        "tanggal_transfer": "Tanggal transfer",
        "nominal": "Nominal",
        "bank_pengirim": "Bank pengirim",
        "nama_pengirim": "Nama pengirim",
    }
    for key, label in required_fields.items():
        if not _required(form, key):
            errors.append(f"{label} wajib diisi.")
    try:
        if form.get("nominal") and float(form.get("nominal")) <= 0:
            errors.append("Nominal harus lebih dari 0.")
    except Exception:
        errors.append("Nominal tidak valid.")
    return errors


def validate_contact_message(form):
    errors = []
    nama = _required(form, "nama")
    pesan = _required(form, "pesan")
    email = _required(form, "email")
    no_hp = _required(form, "no_hp")

    if not nama:
        errors.append("Nama wajib diisi.")
    if not pesan:
        errors.append("Pesan wajib diisi.")
    if email and "@" not in email:
        errors.append("Format email tidak valid.")
    if no_hp and not any(ch.isdigit() for ch in no_hp):
        errors.append("Nomor HP tidak valid.")
    return errors
