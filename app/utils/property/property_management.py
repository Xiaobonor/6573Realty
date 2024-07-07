# app/utils/property/property_management.py
from flask import render_template

from app.models.rental_property import (Negotiation, RentIncludes, Electric, Internet, Water,
                                        ManagementFee, Room, RoomTags, RentalProperty)
from app.models.tags import Tag
from app.models.user import User
from app.utils.agents.chat.image_tag import image_tag
from app.utils.agents.chat.tag_fields_generated import tag_fields_generated
from app.utils.algorithm.tag_algorithm import remove_hash, get_bert_vectors, get_tfidf_vectors, calculate_similarity
from app.utils.mail_sender import send_email


def create_negotiation(data):
    return Negotiation(
        allow=data['negotiation'][0] == 'true',
        min_price=float(data.get('min_price', [0])[0]),
        max_price=float(data.get('max_price', [0])[0])
    )


def create_rent_includes(data):
    return RentIncludes(
        electric=Electric(
            tai_power=data['electric'][0] == 'true',
            price_per_unit=float(data.get('electric_price_per_unit', [0])[0])
        ),
        internet=Internet(
            included=data['internet'][0] == 'true',
            upload_speed=int(data.get('internet_upload_speed', [0])[0]),
            download_speed=int(data.get('internet_download_speed', [0])[0]),
            additional_fee=float(data.get('internet_additional_fee', [0])[0])
        ),
        water=Water(
            included=data['water'][0] == 'true',
            additional_fee=float(data.get('water_additional_fee', [0])[0])
        ),
        management_fee=ManagementFee(
            included=data['management_fee'][0] == 'true',
            additional_fee=float(data.get('management_fee_additional_fee', [0])[0])
        )
    )


async def generate_tags_and_fields(base64s, data):
    image_tag_data, usage = await image_tag(base64s)
    rooms = []

    all_tags = set()

    if image_tag_data.get('success'):
        for room_data in image_tag_data.get('rooms', []):
            tags = RoomTags(
                floor=room_data['tags'].get('floor', []),
                walls=room_data['tags'].get('walls', []),
                view=room_data['tags'].get('view', []),
                furniture=room_data['tags'].get('furniture', []),
                features=room_data['tags'].get('features', []),
                appliances=room_data['tags'].get('appliances', []),
                lighting=room_data['tags'].get('lighting', []),
                decor=room_data['tags'].get('decor', []),
                color_scheme=room_data['tags'].get('color_scheme', []),
                size=room_data['tags'].get('size', []),
                positive=room_data['tags'].get('positive', []),
                negative=room_data['tags'].get('negative', []),
                other=room_data['tags'].get('other', [])
            )

            all_tags.update(room_data['tags'].get('floor', []))
            all_tags.update(room_data['tags'].get('walls', []))
            all_tags.update(room_data['tags'].get('view', []))
            all_tags.update(room_data['tags'].get('furniture', []))
            all_tags.update(room_data['tags'].get('features', []))
            all_tags.update(room_data['tags'].get('appliances', []))
            all_tags.update(room_data['tags'].get('lighting', []))
            all_tags.update(room_data['tags'].get('decor', []))
            all_tags.update(room_data['tags'].get('color_scheme', []))
            all_tags.update(room_data['tags'].get('size', []))
            all_tags.update(room_data['tags'].get('positive', []))
            all_tags.update(room_data['tags'].get('negative', []))
            all_tags.update(room_data['tags'].get('other', []))

            room = Room(
                room_category=room_data['room_category'],
                room_score=int(room_data['room_score']),
                tags=tags
            )
            rooms.append(room)

    generated_fields = {}
    required_fields = {
        'name': '標題',
        'description': '簡述',
        'detailed_description': '詳細描述',
        'furniture': '家具',
        'amenities': '便利設施',
        'decoration_style': '裝修風格'
    }

    data_tag_to_gen = {
        'address': data.get('address', [''])[0]
    }
    data_tag_to_gen.update(image_tag_data)

    for field, description in required_fields.items():
        if not data.get(field) or data.get(field)[0] == '':
            generated_text, usage = await tag_fields_generated(field, data_tag_to_gen)
            generated_fields[field] = generated_text['field_output']

    Tag.in_related_tags("allTags", list(all_tags))

    return generated_fields, rooms, list(all_tags)


def create_rental_property(data, landlord, negotiation, rent_includes, generated_fields, rooms, base64s, all_tags):
    # Calculate BERT and TF-IDF vectors for tags
    bert_vectors = get_bert_vectors(remove_hash(all_tags))
    tfidf_vectors = get_tfidf_vectors(all_tags)

    print("SStart matching with users")
    users = match_with_users(bert_vectors, tfidf_vectors)
    property = RentalProperty.create(
        name=generated_fields.get('name') or data.get('name', [''])[0],
        description=generated_fields.get('description') or data.get('description', [''])[0],
        detailed_description=generated_fields.get('detailed_description') or data.get('detailed_description', [''])[0],
        landlord=landlord,
        furniture=data.get('furniture', generated_fields.get('furniture', '').split(',')),
        amenities=data.get('amenities', generated_fields.get('amenities', '').split(',')),
        address=data['address'][0],
        floor_info=data['floor_info'][0],
        rent_price=int(data['rent_price'][0]),
        deposit=int(data['deposit'][0]),
        negotiation=negotiation,
        property_type=data['property_type'][0],
        layout=data['layout'][0],
        features=data.get('features', []),
        building_type=data['building_type'][0],
        area=float(data['area'][0]),
        rent_includes=rent_includes,
        decoration_style=generated_fields.get('decoration_style') or data.get('decoration_style', [''])[0],
        tenant_preferences=data.get('tenant_preferences', []),
        community=data['community'][0],
        min_lease_months=int(data['min_lease_months'][0]),
        has_balcony=data.get('has_balcony', [generated_fields.get('has_balcony', '')])[0] == 'true',
        images=base64s,
        rooms=rooms,
        allTags=list(all_tags),
        bert_vectors=bert_vectors.tolist(),
        tfidf_vectors=tfidf_vectors.tolist(),
        building_age=int(data.get('building_age', [0])[0])
    )

    for user in users:
        send_email("有與您需求相符的房源！", user.email,
                   "email/match_with_user.html", user=user, property=property)
        print(f"Sent email to {user.email}")

    return property


def match_with_users(bert_vectors, tfidf_vectors):
    users = User.objects(find_rent_property=True)
    user_similarity_scores = []
    print(f"Matching with {len(users)} users")

    for user in users:
        print(f"Matching with user: {user.name}")
        similarity = calculate_similarity(
            bert_vectors,
            user.find_rent_property_detail.bert_vectors,
            tfidf_vectors,
            user.find_rent_property_detail.tfidf_vectors,
        )
        print(f"Similarity with {user.name}: {similarity}")
        user_similarity_scores.append((user, similarity))

    # Sort users by similarity score in descending order
    user_similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # Get the top 50% users
    top_percent_index = int(len(user_similarity_scores) * 0.5)
    best_match = [user for user, score in user_similarity_scores[:top_percent_index]]

    for user, score in user_similarity_scores[:top_percent_index]:
        print(f"Best matched user: {user.name} with similarity score: {score}")

    return best_match
