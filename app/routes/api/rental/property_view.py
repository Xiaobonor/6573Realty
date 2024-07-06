# app/routes/rental/property_view.py
from flask import Blueprint, jsonify, render_template
from app.models.rental_property import RentalProperty

property_view_bp = Blueprint('property_view', __name__)


@property_view_bp.route('/view/<uuid>')
def view_property(uuid):
    print(f"Viewing property: {uuid}")
    property = RentalProperty.get_property_by_uuid(uuid)
    if property:
        property_data = property.to_mongo().to_dict()
        property_data['_id'] = str(property_data['_id'])
        return render_template('property_management/rental/view.html', property_data=property_data)
    else:
        return jsonify({"error": "Property not found"}), 404
