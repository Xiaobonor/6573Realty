# app/routes/rental/property_management.py
from flask import Blueprint, render_template
from app.utils.auth_utils import login_required, seller_required

rent_property_management_bp = Blueprint('rent_property_management', __name__)


@rent_property_management_bp.route('/new')
@login_required
@seller_required
def new_property():
    return render_template('property_management/rental/new.html')
