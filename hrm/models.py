from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django_elasticsearch_dsl.registries import registry


class Company(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name + " " + self.country


class Courses(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='employees')
    current_job = models.CharField(max_length=200)
    year_of_experience = models.FloatField(default=0.0)
    courses = models.ManyToManyField(Courses, related_name='courses')

    @property
    def courses_indexing(self):
        """skills for indexing.

        Used in Elasticsearch indexing.
        """
        return [course.name for course in self.courses.all()]

    @property
    def skills_indexing(self):
        skills = self.skills.all()
        return skills

    def __str__(self):
        return self.name + " " + self.current_job


LEVEL = [
    ('EXPERT', 'Expert'),
    ('BEGINNER', 'Beginner'),
    ('INTERMEDIATE', 'Intermediate'),
]


class Skills(models.Model):
    name = models.CharField(max_length=200)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='skills')
    level = models.CharField(
        max_length=12,
        choices=LEVEL,
        default='BEGINNER',
    )

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name + " " + self.employee.name


@receiver(post_save, sender=Skills)
def update_skills(sender, instance, created, **kwargs):
    registry.update(instance.employee)


@receiver(post_delete, sender=Skills)
def delete_skills(sender, instance, using, **kwargs):
    registry.update(instance.employee)
