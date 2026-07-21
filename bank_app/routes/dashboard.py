from flask import Blueprint, render_template
from ..utils.helpers import login_required, loan_progress
from ..services.dashboard_service import get_stats, get_chart_data, get_recent_activity

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("")
@dashboard_bp.route("/")
@login_required
def dashboard_home():
    stats = get_stats()
    charts = get_chart_data()
    loans, confirmations = get_recent_activity()
    return render_template(
        "dashboard/dashboard.html",
        stats=stats,
        charts=charts,
        loans=loans,
        confirmations=confirmations,
        loan_progress=loan_progress,
    )
