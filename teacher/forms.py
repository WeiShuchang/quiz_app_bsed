from django import forms
from .models import Category, Quiz, Class

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'picture', 'class_assigned']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'picture']


class EditQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'picture']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'description']  # Only include the name field

