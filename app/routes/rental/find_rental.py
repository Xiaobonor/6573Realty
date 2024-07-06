from flask import Blueprint, jsonify, request, render_template
from app.models.rental_property import RentalProperty
from app.models.user import User

find_rental_bp = Blueprint('find_rental', __name__)

@find_rental_bp.route('/tag_user')
def tag_user():
    return render_template('property_management/rental/tag_user.html')

@find_rental_bp.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.json
    user_answers = data.get('answers')

    properties = get_properties_based_on_answers(user_answers)

    if properties:
        return jsonify(success=True, properties=properties)
    else:
        return jsonify(success=False, error='未找到合適的房屋')

@find_rental_bp.route('/submit_selected_properties', methods=['POST'])
def submit_selected_properties():
    data = request.json
    selected_properties = data.get('selected_properties')

    success = process_selected_properties(selected_properties)

    if success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='無法處理選擇的房屋')

def get_properties_based_on_answers(answers):
    properties = RentalProperty.objects(
        property_type=answers['請選擇您想找的房子類型：'],
        layout=answers['請選擇房屋格局：'],
        building_type=answers['請選擇建築類型：']
    ).all()

    return [property.to_dict() for property in properties]

def process_selected_properties(selected_properties):
    for property_uuid in selected_properties:
        property = RentalProperty.get_property_by_uuid(property_uuid)
        if property:
            # 實際的處理邏輯
            pass

    return True
