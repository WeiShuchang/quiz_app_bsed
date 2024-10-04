from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizAttempt, GameQuestion, GameChoice, GameSession, UserScore, Game
from .models import UserProfile  # Import UserProfile for permission check

# Dictionary of models and their respective admin classes
model_admins = {
    Category: admin.ModelAdmin,
    Quiz: admin.ModelAdmin,
    Question: admin.ModelAdmin,
    Choice: admin.ModelAdmin,
    Game: admin.ModelAdmin,
    QuizAttempt: admin.ModelAdmin,
    GameQuestion: admin.ModelAdmin,
    GameChoice: admin.ModelAdmin,
    GameSession: admin.ModelAdmin,
    UserScore: admin.ModelAdmin,

}

# Register each model with its corresponding admin class
for model, admin_class in model_admins.items():
    admin.site.register(model, admin_class)
