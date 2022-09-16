from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .analyzers import html_strip

from hrm.models import (
    Company, Courses, Employee, Skills
)


@registry.register_document
class HRMDocument(Document):
    class Index:
        name = 'hrm_index'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    name = fields.TextField(
        attr='name',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.Completion(),
        }
    )
    company = fields.ObjectField(
        properties={
            'name': fields.TextField(),
            'country': fields.TextField(),
        }
    )
    current_job = fields.TextField(attr='current_job')
    year_of_experience = fields.FloatField()
    courses = fields.TextField(
        attr='courses_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    skills = fields.NestedField(
        attr='skills_indexing',
        properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'level': fields.TextField(
                analyzer=html_strip,
                fields={
                    'raw': fields.KeywordField(),
                },
            ),
        },
    )

    class Django:
        model = Employee
        fields = [
            'id',
        ]

        related_models = [Company]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'company'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Company):
            return related_instance.employees.all()
        elif isinstance(related_instance, Skills):
            return related_instance.skills
