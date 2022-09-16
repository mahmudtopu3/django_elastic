from rest_framework import serializers
from hrm.documents import HRMDocument
from .models import Employee



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 
            'name', 
            'current_job', 
            'year_of_experience', 
            'company', 
            'courses', 
            'skills', 
        )
        depth = 1

