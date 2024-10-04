from django import forms
from .models import Category, Quiz

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'picture']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'picture']


class EditQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'picture']
