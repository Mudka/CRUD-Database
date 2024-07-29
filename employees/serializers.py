from rest_framework import serializers
from .models import Employee
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        # Validation for Workflow value
        if data.get('workflow') is not None and data['workflow'] < 0:
            raise serializers.ValidationError("Workflow cannot be negative")
        # Validtation for required fields (name & department)
        if not data.get('name'):
            raise serializers.ValidationError("Name is a required field.")
        if not data.get("department"):
            raise serializers.ValidationError("Department is a required field.")
        # Checks if an Employee already exists in the department
        if not self.instance:
            name = data.get('name')
            department = data.get('department')
            if Employee.objects.filter(name=name, department=department).exists():
                raise serializers.ValidationError("An employee with this name already exists in this department")
        return data
    
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token