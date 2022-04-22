from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'birth_date']
