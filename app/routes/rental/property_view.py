# app/routes/rental/property_view.py
from flask import Blueprint, jsonify, render_template
from app.models.rental_property import RentalProperty
from app.models.user import User

property_view_bp = Blueprint('property_view', __name__)


@property_view_bp.route('/view/<uuid>')
def view_property(uuid):
    print(f"Viewing property: {uuid}")
    property = RentalProperty.get_property_by_uuid(uuid)
    print_property = property
    # remove
    print(print_property)
    if property:
        landlord = User.objects(google_id=property.landlord.google_id).first()
        landlord_name = landlord.name if landlord else '未知'
        landlord_company = landlord.sell_rent_property_detail.company if landlord and landlord.sell_rent_property else '無'
        landlord_info = f"{landlord_name} ({landlord_company})"

        property_data = property.to_mongo().to_dict()
        property_data['_id'] = str(property_data['_id'])
        property_data['landlord_info'] = landlord_info
        property_data['landlord_line'] = landlord.sell_rent_property_detail.line if landlord else '無'
        return render_template('property_management/rental/view.html', property_data=property_data)
    else:
        return jsonify({"error": "Property not found"}), 404
