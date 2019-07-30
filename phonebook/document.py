from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import *


@registry.register_document
class ContactDocument(Document):
    number_ids = fields.NestedField(properties={
        'number': fields.TextField(),
        'number_type': fields.TextField(),
    })

    class Index:
        name = 'contacts'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Contact
        fields = ['fname', 'lname', 'email', 'bdate', 'company_name', 'website', 'is_favourite']
        related_models = [ContactNo]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ContactNo):
            return related_instance.contact_id
