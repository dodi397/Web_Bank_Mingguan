from ..extensions import db
from ..models import SiteSetting

def get_site_setting():
    setting = SiteSetting.query.first()
    if setting is None:
        setting = SiteSetting()
        db.session.add(setting)
        db.session.commit()
    return setting

def update_site_setting(setting, form):
    setting.address = (form.get("address") or "").strip()
    setting.contact_phone = (form.get("contact_phone") or "").strip()
    setting.contact_email = (form.get("contact_email") or "").strip()
    setting.contact_note = (form.get("contact_note") or "").strip() or None
    db.session.commit()
    return setting
