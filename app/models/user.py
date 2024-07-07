# app/models/user.py
from datetime import datetime
from mongoengine import Document, StringField, URLField, EmailField, DateTimeField, BooleanField, EmbeddedDocument, \
    IntField, EmbeddedDocumentField, ListField, FloatField


class FindRentProperty(EmbeddedDocument):
    max_price = IntField(required=True)
    location = ListField(required=True)  # City and District name
    target_location = StringField(required=False)  # school or company location, why they want to rent the property
    property_type = ListField(choices=['entire_home', 'studio', 'shared_room'], required=True)
    layout = ListField(choices=['1_room', '2_rooms', '3_rooms', '4_rooms'], required=True)
    building_type = ListField(choices=['apartment', 'elevator_building', 'townhouse', 'villa', 'N/A'], required=True)
    tags = ListField(required=True)
    bert_vectors = ListField(ListField(FloatField()), required=True)
    tfidf_vectors = ListField(ListField(FloatField()), required=True)


class Sellers(EmbeddedDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    line = StringField(required=True)
    company = StringField(required=True)
    email = EmailField(required=True)


class User(Document):
    google_id = StringField(required=True, primary_key=True)
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    avatar_url = URLField(required=True)

    find_rent_property = BooleanField(required=True)
    find_rent_property_detail = EmbeddedDocumentField(FindRentProperty)

    sell_rent_property = BooleanField(required=True)
    sell_rent_property_detail = EmbeddedDocumentField(Sellers)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users'}

    @classmethod
    def create_user(cls, google_id, email, name, avatar_url):
        """
        Create a new user with the given information.
        :param google_id: Google ID of the user.
        :param email: Email address of the user.
        :param name: Name of the user.
        :param avatar_url: Photo URL of the user.
        """
        try:
            user = cls(
                google_id=google_id,
                email=email,
                name=name,
                avatar_url=avatar_url,
                find_rent_property=False,
                sell_rent_property=False
            )
            user.save()
            return user
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_user_by_email(cls, email):
        """
        Retrieve a user by their email address.
        :param email: Email address of the user.
        :return: User object if found, None otherwise.
        """
        return cls.objects(email=email).first()
