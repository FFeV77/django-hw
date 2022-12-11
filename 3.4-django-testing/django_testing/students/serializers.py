from rest_framework import serializers
from rest_framework.settings import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        q = Course.objects.filter(students=value).count()
        max_students_per_course = settings('MAX_STUDENTS_PER_COURSE')
        if q >= max_students_per_course:
            raise serializers.ValidationError('Достигнут лимит студентов на курсе')
