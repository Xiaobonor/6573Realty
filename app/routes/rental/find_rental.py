from flask import Blueprint, jsonify, request, render_template, session
from app.models.rental_property import RentalProperty
from app.models.user import User, FindRentProperty
from app.utils.auth_utils import login_required
from app.utils.algorithm.tag_algorithm import get_bert_vectors, get_tfidf_vectors, remove_hash

find_rental_bp = Blueprint('find_rental', __name__)


@find_rental_bp.route('/tag_user')
@login_required
def tag_user():
    return render_template('property_management/rental/tag_user.html')


@find_rental_bp.route('/submit_answers', methods=['POST'])
@login_required
def submit_answers():
    data = request.json
    user_answers = data.get('answers')
    session['user_answers'] = user_answers

    properties = get_properties_based_on_answers(user_answers)

    if properties:
        return jsonify(success=True, properties=properties)
    else:
        return jsonify(success=False, error='未找到合適的房屋')


@find_rental_bp.route('/submit_selected_properties', methods=['POST'])
@login_required
def submit_selected_properties():
    data = request.json
    selected_properties = data.get('selected_properties')

    success, userTags = process_selected_properties(selected_properties)
    user_id = session['user_info']['google_id']
    user = User.objects(google_id=user_id).first()

    max_price = int(session['user_answers']['請輸入您接受的最高租金價格：'])
    location = session['user_answers']['請輸入您的租屋預計位置：']
    property_type = ''.join(session['user_answers']['請選擇您想找的房子類型：']).split(',')
    layout = ''.join(session['user_answers']['請選擇房屋格局：']).split(',')
    building_type = ''.join(session['user_answers']['請選擇建築類型：']).split(',')

    valid_property_types = ['entire_home', 'studio', 'shared_room']
    valid_layouts = ['1_room', '2_rooms', '3_rooms', '4_rooms']
    valid_building_types = ['apartment', 'elevator_building', 'townhouse', 'villa', 'N/A']

    property_type = [pt for pt in property_type if pt in valid_property_types]
    layout = [lt for lt in layout if lt in valid_layouts]
    building_type = [bt for bt in building_type if bt in valid_building_types]

    if not property_type or not layout or not building_type:
        return jsonify(success=False, error='所選的房屋類型、格局或建築類型無效')

    user.find_rent_property = True
    user.find_rent_property_detail = FindRentProperty(
        max_price=max_price,
        location=[location],
        property_type=property_type,
        layout=layout,
        building_type=building_type,
        tags=userTags,
        bert_vectors=get_bert_vectors(remove_hash(userTags)),
        tfidf_vectors=get_tfidf_vectors(remove_hash(userTags))
    )
    user.save()

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
    user_tags = set()
    for property_uuid in selected_properties:
        property = RentalProperty.get_property_by_uuid(property_uuid)
        if not property:
            return False, None

        property_tags = property.allTags
        user_tags.update(property_tags)

    return True, list(user_tags)
