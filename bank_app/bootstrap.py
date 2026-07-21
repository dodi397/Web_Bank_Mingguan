from .extensions import db
from .models import Admin, Nasabah, PaymentSetting, SiteSetting
from .services.pinjaman_service import create_pinjaman

def seed_data(app):
    with app.app_context():
        db.create_all()

        if not Admin.query.first():
            admin = Admin(username=app.config["ADMIN_USERNAME"], nama=app.config["ADMIN_NAMA"])
            admin.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(admin)
            db.session.commit()

        if not PaymentSetting.query.first():
            payment_setting = PaymentSetting(
                bank_name=app.config["BANK_NAME"],
                account_name=app.config["ACCOUNT_NAME"],
                account_number=app.config["ACCOUNT_NUMBER"],
                qris_label=app.config["QRIS_TEXT"],
            )
            db.session.add(payment_setting)
            db.session.commit()

        if not SiteSetting.query.first():
            site_setting = SiteSetting(
                address=app.config["ADDRESS"],
                contact_phone=app.config["CONTACT_PHONE"],
                contact_email=app.config["CONTACT_EMAIL"],
            )
            db.session.add(site_setting)
            db.session.commit()

        if not Nasabah.query.first():
            nasabah1 = Nasabah(
                nama="Andi Saputra",
                nik="3174012345678901",
                alamat="Jl. Melati No. 1, Jakarta",
                no_hp="081234567890",
                pekerjaan="Wiraswasta",
            )
            nasabah2 = Nasabah(
                nama="Rina Dewi",
                nik="3174012345678902",
                alamat="Jl. Kenanga No. 5, Bandung",
                no_hp="081234567891",
                pekerjaan="Pegawai Swasta",
            )
            nasabah3 = Nasabah(
                nama="Budi Santoso",
                nik="3174012345678903",
                alamat="Jl. Mawar No. 7, Bekasi",
                no_hp="081234567892",
                pekerjaan="Pedagang",
            )
            db.session.add_all([nasabah1, nasabah2, nasabah3])
            db.session.commit()

            loan1 = create_pinjaman(nasabah1.id, 10000000, 2, 12)
            loan2 = create_pinjaman(nasabah2.id, 8000000, 1.5, 10)
            loan3 = create_pinjaman(nasabah3.id, 5000000, 2.0, 8)
            loan3.status = "Lunas"
            loan3.sisa_tagihan = 0
            db.session.commit()
