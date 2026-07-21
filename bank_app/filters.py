from .utils.formatter import badge_class, format_date, percent, rupiah

def register_jinja_filters(app):
    app.jinja_env.filters["rupiah"] = rupiah
    app.jinja_env.filters["tanggal"] = format_date
    app.jinja_env.filters["badge"] = badge_class
    app.jinja_env.filters["percent"] = percent
