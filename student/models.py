from django.db import models
from teacher.models import User, Class
from django.contrib.auth.models import User

# Create your models here.
class StudentClass(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_classes')
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrolled_students')

    class Meta:
        unique_together = ('student', 'classroom')

    def __str__(self):
        return f"{self.student.username} - {self.classroom.name}"