from .services.payment_setting_service import get_payment_setting
from .services.site_setting_service import get_site_setting

def register_context_processors(app):
    @app.context_processor
    def inject_globals():
        payment_setting = get_payment_setting()
        site_setting = get_site_setting()
        return {
            "app_name": app.config["BANK_NAME"],
            "payment_setting": payment_setting,
            "site_setting": site_setting,
            "account_name": payment_setting.account_name or app.config["ACCOUNT_NAME"],
            "account_number": payment_setting.account_number or app.config["ACCOUNT_NUMBER"],
            "qris_text": payment_setting.qris_label or app.config["QRIS_TEXT"],
            "contact_email": site_setting.contact_email or app.config["CONTACT_EMAIL"],
            "contact_phone": site_setting.contact_phone or app.config["CONTACT_PHONE"],
            "address": site_setting.address or app.config["ADDRESS"],
        }
