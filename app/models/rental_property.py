from datetime import datetime
from mongoengine import Document, StringField, UUIDField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, IntField, FloatField, BooleanField, URLField, DateTimeField
import uuid


class Negotiation(EmbeddedDocument):
    allow = BooleanField(required=True)
    min_price = FloatField(required=True)
    max_price = FloatField(required=True)


class Allowance(EmbeddedDocument):
    allow = BooleanField(required=True)
    additional_fee = FloatField(required=True)


class Electric(EmbeddedDocument):
    tai_power = BooleanField(required=True)
    price_per_unit = FloatField(required=True)


class Internet(EmbeddedDocument):
    included = BooleanField(required=True)
    upload_speed = IntField(required=True)
    download_speed = IntField(required=True)
    additional_fee = FloatField(required=True)


class Water(EmbeddedDocument):
    included = BooleanField(required=True)
    additional_fee = FloatField(required=True)


class ManagementFee(EmbeddedDocument):
    included = BooleanField(required=True)
    additional_fee = FloatField(required=True)


class RentIncludes(EmbeddedDocument):
    electric = EmbeddedDocumentField(Electric, required=True)
    internet = EmbeddedDocumentField(Internet, required=True)
    water = EmbeddedDocumentField(Water, required=True)
    management_fee = EmbeddedDocumentField(ManagementFee, required=True)


class RoomTags(EmbeddedDocument):
    floor = ListField(StringField())
    walls = ListField(StringField())
    view = ListField(StringField())
    furniture = ListField(StringField())
    features = ListField(StringField())
    appliances = ListField(StringField())
    lighting = ListField(StringField())
    decor = ListField(StringField())
    color_scheme = ListField(StringField())
    size = ListField(StringField())
    positive = ListField(StringField())
    negative = ListField(StringField())
    other = ListField(StringField())


class Room(EmbeddedDocument):
    room_category = StringField(choices=[
        'bedroom', 'bathroom', 'living_room', 'kitchen', 'dining_room',
        'study', 'guest_room', 'laundry_room', 'garage', 'balcony', 'garden',
        'hallway', 'exterior'
    ], required=True)
    room_score = IntField(min_value=0, max_value=100, required=True)
    tags = EmbeddedDocumentField(RoomTags, required=True)


class RentalProperty(Document):
    # UUID
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, required=True)

    # Basic Info
    name = StringField(required=True)
    description = StringField(required=True)
    detailed_description = StringField(required=True)
    landlord = ReferenceField('User', required=True)

    # Address
    address = StringField(required=True)
    floor_info = StringField(required=True)  # e.g., "3/5"

    # Price
    rent_price = FloatField(required=True)
    negotiation = EmbeddedDocumentField(Negotiation, required=True)

    # Property Type
    property_type = StringField(choices=['entire_home', 'studio', 'shared_room'], required=True)
    layout = StringField(choices=['1_room', '2_rooms', '3_rooms', '4_rooms'], required=True)
    building_type = StringField(choices=['apartment', 'elevator_building', 'townhouse', 'villa'], required=True)

    # Area
    furniture = ListField(StringField(), required=True)
    amenities = ListField(StringField(), required=True)
    rent_includes = EmbeddedDocumentField(RentIncludes, required=True)
    allowances = EmbeddedDocumentListField(Allowance, required=True)
    features = ListField(StringField(required=True))
    # features = ListField(StringField(choices=['allow_cooking', 'allow_pets', 'balcony']), required=True)
    decoration_style = StringField(required=True)
    images = ListField(StringField(), required=True)
    rooms = EmbeddedDocumentListField(Room, required=True)
    area = FloatField(required=True)

    # Other
    tenant_preferences = ListField(StringField(
        choices=['male_only', 'female_only', 'no_night_life', 'students_only', 'working_professionals_only',
                 'others']), required=True)
    community = StringField(required=True)
    min_lease_months = IntField(required=True)
    has_balcony = BooleanField(required=True)
    bathroom_info = StringField()  # Optional
    building_age = IntField()  # Optional
    display_tags = ListField(StringField(), required=True)
    view_count = IntField(default=0, required=True)

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow, required=True)
    last_updated_at = DateTimeField(default=datetime.utcnow, required=True)
    last_pushed_at = DateTimeField()

    meta = {'collection': 'rental_properties'}

    @classmethod
    def create(cls, name, description, detailed_description, landlord, furniture, amenities, address, floor_info,
               rent_price, negotiation, property_type, layout, allowances, features, building_type, area, rent_includes,
               decoration_style, tenant_preferences, community, min_lease_months, has_balcony, images, rooms,
               bathroom_info=None, building_age=None, display_tags=None):
        rental_property = cls(
            name=name,
            description=description,
            detailed_description=detailed_description,
            landlord=landlord,
            furniture=furniture,
            amenities=amenities,
            address=address,
            floor_info=floor_info,
            rent_price=rent_price,
            negotiation=negotiation,
            property_type=property_type,
            layout=layout,
            allowances=allowances,
            features=features,
            building_type=building_type,
            area=area,
            rent_includes=rent_includes,
            decoration_style=decoration_style,
            tenant_preferences=tenant_preferences,
            community=community,
            min_lease_months=min_lease_months,
            has_balcony=has_balcony,
            bathroom_info=bathroom_info,
            building_age=building_age,
            display_tags=display_tags or [],
            images=images,
            rooms=rooms
        )
        rental_property.save()
        return rental_property
