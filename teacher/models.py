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

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='category_pictures/', blank=True, null=True)
   
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
    picture = models.ImageField(upload_to='choices_picture/', null=True, blank=True)
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



class Game(models.Model):
    name = models.CharField(max_length=255)  # Name of the game
    total_questions = models.IntegerField(default=20)  # Total number of questions in the game
    duration = models.IntegerField(default=120)  # Duration of the game in seconds
    description = models.TextField(blank=True, null=True)  # Description of the game
    picture = models.ImageField(upload_to='game_pictures/', null=True, blank=True)  # Game image

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
        return self.name

class GameQuestion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=1024)

    def __str__(self):
        return self.text

class GameChoice(models.Model):
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE, related_name='game_choices')
    text = models.CharField(max_length=1024)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class GameSession(models.Model):
    player_name = models.CharField(max_length=255)  # Store the player's name
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)
    current_question = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.player_name}'s Game on {self.date_played}"

class UserScore(models.Model):
    player_name = models.CharField(max_length=255)  # Store the player's name
    score = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name}: {self.score} on {self.date_recorded}"