# app/routes/rental/property_management.py
import asyncio
from flask import Blueprint, request, session, flash, jsonify, redirect, url_for
from app.utils.auth_utils import login_required
from app.utils.property.property_management import (
    create_negotiation,
    create_rent_includes,
    generate_tags_and_fields,
    create_rental_property
)

api_rent_property_management_bp = Blueprint('api_rent_property_management', __name__)


@api_rent_property_management_bp.route('/new', methods=['POST'])
@login_required
def create_property():
    try:
        print("Creating property")
        data = request.form.to_dict(flat=False)
        landlord = session['user_info']['google_id']

        negotiation = create_negotiation(data)
        rent_includes = create_rent_includes(data)

        print("Rent Includes: ", rent_includes)

        base64s = request.form.getlist('images')
        print("Base64s: ", len(base64s))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        generated_fields, rooms = loop.run_until_complete(generate_tags_and_fields(base64s, data))

        rental_property = create_rental_property(data, landlord, negotiation, rent_includes, generated_fields, rooms, base64s)

        print("Property created: ", rental_property.id)
        flash('租屋物件建立成功!', 'popup_success')
        return jsonify({'success': True, 'uuid': str(rental_property.id),
                        'redirect_url': f'{redirect(url_for("rent_property_management.view_property", uuid=str(rental_property.id)))}'})
    except Exception as e:
        flash(f'建立租屋物件時發生錯誤: {str(e)}', 'popup_error')
        print("----------------------------------------------")
        print(f"Error creating property: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
