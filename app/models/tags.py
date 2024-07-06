# app/models/tags.py
from mongoengine import Document, StringField, ListField


class Tag(Document):
    name = StringField(required=True, unique=True)
    related_tags = ListField(StringField())

    meta = {'collection': 'tags'}

    @classmethod
    def get_all_related_tags(cls, name):
        tag = cls.objects(name=name).first()
        if not tag:
            return []
        return tag.related_tags

    @classmethod
    def get_or_create_tag_by_name(cls, name):
        tag = cls.objects(name=name).first()
        if not tag:
            tag = cls(name=name)
            tag.save()
        return tag

    @classmethod
    def in_related_tags(cls, name, tag_list):
        tag = cls.get_or_create_tag_by_name(name)
        if not tag:
            return Exception("Tag not found")

        tag.in_related_tags_list(tag_list)

    # check is the tag in the related_tags list? yes add it in (input list)
    def in_related_tags_list(self, tag_list):
        for tag_name in tag_list:
            if tag_name not in self.related_tags:
                self.related_tags.append(tag_name)
        self.save()

    def __str__(self):
        return self.name
