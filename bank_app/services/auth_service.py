from werkzeug.security import check_password_hash
from ..models import Admin


def authenticate_admin(username: str, password: str):
    admin = Admin.query.filter_by(username=username).first()
    if admin and check_password_hash(admin.password, password):
        return admin
    return None
