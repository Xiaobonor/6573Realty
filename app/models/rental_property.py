# app/models/rental_property.py
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


class RentIncludes(EmbeddedDocument):
    electric = EmbeddedDocumentField(
        EmbeddedDocumentField('Electric', required=True))
    internet = EmbeddedDocumentField(
        EmbeddedDocumentField('Internet', required=True))
    water = EmbeddedDocumentField(EmbeddedDocumentField('Water', required=True))
    management_fee = EmbeddedDocumentField(
        EmbeddedDocumentField('ManagementFee', required=True))


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


class Image(EmbeddedDocument):
    url = URLField(required=True)
    title = StringField(required=True)


class RoomTags(EmbeddedDocument):
    floor = ListField(StringField(), required=True)
    walls = ListField(StringField(), required=True)
    view = ListField(StringField(), required=True)
    furniture = ListField(StringField(), required=True)
    features = ListField(StringField(), required=True)
    appliances = ListField(StringField(), required=True)
    lighting = ListField(StringField(), required=True)
    decor = ListField(StringField(), required=True)
    color_scheme = ListField(StringField(), required=True)
    size = ListField(StringField(), required=True)
    other = ListField(StringField(), required=True)


class Room(EmbeddedDocument):
    room_category = StringField(choices=[
        'bedroom', 'bathroom', 'living_room', 'kitchen', 'dining_room',
        'study', 'guest_room', 'laundry_room', 'garage', 'balcony', 'garden',
        'hallway', 'exterior'
    ], required=True)
    room_score = IntField(min_value=0, max_value=100, required=True)
    tags = EmbeddedDocumentField(RoomTags, required=True)


class RentalProperty(Document):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    detailed_description = StringField(required=True)
    landlord = ReferenceField('User', required=True)
    furniture = ListField(StringField(), required=True)
    amenities = ListField(StringField(), required=True)
    address = StringField(required=True)
    floor_info = StringField(required=True)  # e.g., "3/5"
    rent_price = FloatField(required=True)
    negotiation = EmbeddedDocumentField(Negotiation, required=True)
    property_type = StringField(choices=['entire_home', 'studio', 'shared_room'], required=True)
    layout = StringField(choices=['1_room', '2_rooms', '3_rooms', '4_rooms'], required=True)
    allowances = EmbeddedDocumentListField(Allowance, required=True)
    features = ListField(StringField(choices=['allow_cooking', 'allow_pets', 'balcony']), required=True)
    building_type = StringField(choices=['apartment', 'elevator_building', 'townhouse', 'villa'], required=True)
    area = FloatField(required=True)
    rent_includes = EmbeddedDocumentField(RentIncludes, required=True)
    decoration_style = StringField(required=True)
    tenant_preferences = ListField(StringField(choices=['male_only', 'female_only', 'no_night_life', 'students_only', 'working_professionals_only', 'others']), required=True)
    community = StringField(required=True)
    min_lease_months = IntField(required=True)
    has_balcony = BooleanField(required=True)
    bathroom_info = StringField()  # Optional
    building_age = IntField()  # Optional
    tags = ListField(StringField(), required=True)
    created_at = DateTimeField(default=datetime.utcnow, required=True)
    last_updated_at = DateTimeField(default=datetime.utcnow, required=True)
    last_pushed_at = DateTimeField()
    images = EmbeddedDocumentListField(Image, required=True)
    view_count = IntField(default=0, required=True)
    rooms = EmbeddedDocumentListField(Room, required=True)

    meta = {'collection': 'rental_properties'}
