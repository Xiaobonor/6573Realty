# app/routes/rental/property_management.py
import asyncio
from flask import Blueprint, request, session, flash, jsonify, redirect, url_for
from app.utils.auth_utils import login_required
from app.models.rental_property import (RentalProperty, Negotiation, RentIncludes, Electric, Internet, Water,
                                        ManagementFee, Room, RoomTags)
from app.utils.agents.chat.image_tag import image_tag
from app.utils.agents.chat.tag_fields_generated import tag_fields_generated

api_rent_property_management_bp = Blueprint('api_rent_property_management', __name__)


@api_rent_property_management_bp.route('/new', methods=['POST'])
@login_required
def create_property():
    try:
        print("Creating property")
        data = request.form.to_dict(flat=False)
        landlord = session['user_info']['google_id']

        negotiation = Negotiation(
            allow=data['negotiation'][0] == 'true',
            min_price=float(data.get('min_price', [0])[0]),
            max_price=float(data.get('max_price', [0])[0])
        )

        rent_includes = RentIncludes(
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

        print("Rent Includes: ", rent_includes)

        base64s = request.form.getlist('images')
        print("Base64s: ", len(base64s))
        image_tag_data, usage = asyncio.run(image_tag(base64s))

        print("Image Tag Data: ", image_tag_data)
        rooms = []
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
                generated_text, usage = asyncio.run(tag_fields_generated(field, data_tag_to_gen))
                print(f"Generated {field}: {generated_text['field_output']}")
                generated_fields[field] = generated_text['field_output']
                print(f"Generated Done: {generated_fields.get(field)}")

        rental_property = RentalProperty.create(
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
            building_age=int(data.get('building_age', [0])[0])
        )

        print("Property created: ", rental_property.id)
        flash('租屋物件建立成功!', 'popup_success')
        return jsonify({'success': True, 'uuid': str(rental_property.id),
                        'redirect_url': f'{redirect(url_for("rent_property_management.view_property", uuid=str(rental_property.id)))}'})
    except Exception as e:
        flash(f'建立租屋物件時發生錯誤: {str(e)}', 'popup_error')
        print("----------------------------------------------")
        print(f"Error creating property: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
