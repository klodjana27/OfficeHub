from rest_framework import serializers
from django.contrib.auth import get_user_model

Employee = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'role', 'department', 'password', 'must_change_password']
        extra_kwargs = {
            'password': {'write_only': True},  # Fjalëkalimi nuk do të shfaqet në përgjigje
            'must_change_password': {'read_only': True}  # Vetëm serveri mund ta ndryshojë këtë fushë
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Employee(**validated_data)
        if password:
            user.set_password(password)  # Siguron që fjalëkalimi të ruhet i koduar
        user.must_change_password = True  # Detyron ndryshimin e fjalëkalimit në login
        user.save()
        return user