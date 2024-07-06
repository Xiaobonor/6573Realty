# app/routes/seller/register.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from mongoengine import ValidationError

from app.models.user import User, Sellers
from app.utils.auth_utils import login_required

seller_register_bp = Blueprint('seller_register', __name__)


@seller_register_bp.route('/seller/register')
@login_required
def register():
    if session['user_info']['sell_rent_property']:
        return redirect(url_for('index.home'))
    return render_template('seller/seller_register.html')


@seller_register_bp.route('/api/v1/seller/register_seller', methods=['POST'])
@login_required
def register_seller():
    if session['user_info']['sell_rent_property']:
        return jsonify({"error": "User is not eligible to sell property"}), 403

    data = request.get_json()
    try:
        user = User.objects(google_id=session['user_info']['google_id']).first()
        print(user)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.sell_rent_property:
            return jsonify({"error": "User is registered as a seller"}), 400

        seller_detail = Sellers(
            name=data['name'],
            phone=data['phone'],
            line=data['line'],
            company=data['company'],
            email=data['email']
        )
        user.sell_rent_property = True
        user.sell_rent_property_detail = seller_detail
        user.save()

        session['user_info']['sell_rent_property'] = True
        session['user_info']['sell_rent_property_detail'] = seller_detail.to_json()

        return jsonify({"message": "Seller registered successfully"}), 200

    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
