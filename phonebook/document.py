from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import DocType, Index, fields

from .models import *

contact = Index('test_contacts')

contact.settings(
    number_of_shards=1,
    number_of_replicas=0
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@contact.doc_type
class ContactDocument(DocType):
    contact_nos = fields.NestedField(properties={
        'numner': fields.TextField(analyzer=html_strip),
        'number_type': fields.TextField(),
        'pk': fields.IntegerField(),
    })

    class Meta:
        model = Contact
        related_models = [ContactNo]
        fields = [
            'fname',
            'lname',
            'email',
            'is_favourite',
        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ContactNo):
            return related_instance.car

        # otherwise it's a Manufacturer or a Category
        return related_instance.contact_set.all()


class ContactNoDocument(DocType):
    description = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )

    class Meta:
        model = ContactNo
        index = 'test_contact_nos'
        fields = [
            'number',
            'number_type',
        ]