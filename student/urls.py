from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name="student_dashboard"),
    path('quiz_student/<int:quiz_id>/', views.quiz_detail, name='quiz_detail_student'),
    path('quiz_student/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),
    path('quiz_student/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]