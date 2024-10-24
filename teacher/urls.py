from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name="teacher_dashboard"),
    path('categories/', views.category_dashboard, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('quizzes_teacher/', views.quiz_list, name='quiz_list_teacher'),
    path('quizzes/create/', views.quiz_create, name='quiz_create'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/add-choice/', views.add_choice, name='add_choice'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('delete_choice/', views.delete_choice, name='delete_choice'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    
]