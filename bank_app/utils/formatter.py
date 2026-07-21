from datetime import date, datetime

MONTHS_ID = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


def rupiah(value) -> str:
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        value = 0
    return f"Rp{value:,.0f}".replace(",", ".")


def format_date(value) -> str:
    if not value:
        return "-"
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value).date()
        except ValueError:
            return value
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return f"{value.day:02d} {MONTHS_ID[value.month]} {value.year}"
    return str(value)


def badge_class(status: str) -> str:
    mapping = {
        "Aktif": "bg-success-subtle text-success",
        "Lunas": "bg-primary-subtle text-primary",
        "Menunggu": "bg-warning-subtle text-warning",
        "Diterima": "bg-success-subtle text-success",
        "Ditolak": "bg-danger-subtle text-danger",
    }
    return mapping.get(status, "bg-secondary-subtle text-secondary")


def percent(value) -> str:
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "0%"
