from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from userprofile.models import UserProfile

# Create your models here.
class Class(models.Model):
    code = models.CharField(max_length=7, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a class can have only one teacher

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super(Class, self).save(*args, **kwargs)

    def generate_unique_code(self):
        length = 7
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(length))
        while Class.objects.filter(code=code).exists():
            code = ''.join(random.choice(characters) for _ in range(length))
        return code


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='category_pictures/', blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='categories', null=True, blank=True) 

    def save(self, *args, **kwargs):
        # Resize image if necessary
        if self.picture:
            image = Image.open(self.picture)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            base_width = 667
            base_height = 1000
            image = image.resize((base_width, base_height), Image.Resampling.LANCZOS)
            
            # Save image back to the file
            temp_file = BytesIO()
            image.save(temp_file, format='JPEG')
            temp_file.seek(0)
            self.picture.save(self.picture.name, ContentFile(temp_file.read()), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    picture = models.ImageField(upload_to='quizzes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Resize image if necessary
        if self.picture:
            image = Image.open(self.picture)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            base_width = 1280
            base_height = 853
            image = image.resize((base_width, base_height), Image.Resampling.LANCZOS)
            
            # Save image back to the file
            temp_file = BytesIO()
            image.save(temp_file, format='JPEG')
            temp_file.seek(0)
            self.picture.save(self.picture.name, ContentFile(temp_file.read()), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    text = models.CharField(max_length=1024)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=1024)
    is_correct = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    score = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attempts')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

