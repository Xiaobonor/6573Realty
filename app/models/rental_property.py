# app/models/rental_property.py
from datetime import datetime
from mongoengine import Document, StringField, UUIDField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, IntField, FloatField, BooleanField, URLField, DateTimeField
import uuid


class Negotiation(EmbeddedDocument):
    allow = BooleanField(required=True)
    min_price = FloatField(required=True)
    max_price = FloatField(required=True)


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
    rent_price = IntField(required=True)
    deposit = IntField(required=True)
    negotiation = EmbeddedDocumentField(Negotiation, required=True)

    # Property Type
    property_type = StringField(choices=['entire_home', 'studio', 'shared_room'], required=True)
    layout = StringField(choices=['1_room', '2_rooms', '3_rooms', '4_rooms'], required=True)
    building_type = StringField(choices=['apartment', 'elevator_building', 'townhouse', 'villa'], required=True)

    # Area
    furniture = ListField(StringField(choices=[
        'sofa', 'bed', 'desk_chair', 'dining_table', 'wardrobe', 'bookshelf',
        'tv_stand', 'nightstand', 'dresser', 'shoe_rack'
    ]), required=False)
    amenities = ListField(StringField(choices=[
        'wifi', 'washing_machine', 'refrigerator', 'water_heater', 'microwave', 'air_conditioner',
        'heater', 'tv', 'dishwasher', 'oven', 'fan',
        'air_purifier', 'fire_extinguisher', 'smoke_detector', 'electric_stove'
    ]), required=False)
    rent_includes = EmbeddedDocumentField(RentIncludes, required=True)
    features = ListField(StringField(required=True))
    # features = ListField(StringField(choices=['allow_cooking', 'allow_pets', 'balcony']), required=True)
    decoration_style = StringField(required=True)
    images = ListField(StringField(), required=True)
    rooms = EmbeddedDocumentListField(Room, required=True)
    area = FloatField(required=True)

    # Other
    tenant_preferences = ListField(StringField(
        choices=['male_only', 'female_only', 'no_night_life', 'students_only', 'working_professionals_only',
                 'others']), required=False)
    community = StringField(required=False)
    min_lease_months = IntField(required=True)
    has_balcony = BooleanField(required=True)
    building_age = IntField()  # Optional
    display_tags = ListField(StringField())
    view_count = IntField(default=0, required=True)

    # Tags BERT and TF-IDF vectors
    bert_vectors = ListField(ListField(FloatField()), required=True)
    tfidf_vectors = ListField(ListField(FloatField()), required=True)

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow, required=True)
    last_updated_at = DateTimeField(default=datetime.utcnow, required=True)
    last_pushed_at = DateTimeField()

    meta = {'collection': 'rental_properties'}

    @classmethod
    def get_property_by_uuid(cls, uuid):
        return cls.objects(uuid=uuid).first()

    @classmethod
    def create(cls, name, description, detailed_description, landlord, address, floor_info,
               rent_price, negotiation, property_type, layout, features, building_type, area, rent_includes,
               decoration_style, min_lease_months, has_balcony, images, rooms, deposit, bert_vectors, tfidf_vectors,
               building_age=None, display_tags=None, amenities=None, tenant_preferences=None, community=None, furniture=None):
        if amenities is None or amenities == "":
            amenities = []
        if tenant_preferences is None or tenant_preferences == "":
            tenant_preferences = []
        if community is None or community == "":
            community = ""
        if furniture is None or furniture == "":
            furniture = []

        valid_amenities = [
            'wifi', 'washing_machine', 'refrigerator', 'water_heater', 'microwave', 'air_conditioner',
            'heater', 'tv', 'dishwasher', 'oven', 'fan',
            'air_purifier', 'fire_extinguisher', 'smoke_detector', 'electric_stove'
        ]
        filtered_amenities = [amenity for amenity in amenities if amenity in valid_amenities]
        valid_furniture = [
            'sofa', 'bed', 'desk_chair', 'dining_table', 'wardrobe', 'bookshelf',
            'tv_stand', 'nightstand', 'dresser', 'shoe_rack'
        ]
        filtered_furniture = [furniture for furniture in furniture if furniture in valid_furniture]

        rental_property = cls(
            name=name,
            description=description,
            detailed_description=detailed_description,
            landlord=landlord,
            furniture=filtered_furniture,
            amenities=filtered_amenities,
            address=address,
            floor_info=floor_info,
            rent_price=rent_price,
            deposit=deposit,
            negotiation=negotiation,
            property_type=property_type,
            layout=layout,
            features=features,
            building_type=building_type,
            area=area,
            rent_includes=rent_includes,
            decoration_style=decoration_style,
            tenant_preferences=tenant_preferences,
            community=community,
            min_lease_months=min_lease_months,
            has_balcony=has_balcony,
            building_age=building_age,
            display_tags=display_tags or [],
            images=images,
            rooms=rooms,
            bert_vectors=bert_vectors,
            tfidf_vectors=tfidf_vectors
        )
        rental_property.save()
        return rental_property
