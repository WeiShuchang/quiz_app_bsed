"""
URL configuration for quiz_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import views, settings


urlpatterns = [
    path('', views.home, name="landing"),

    #authentication
    path('login_page/', views.login_view, name='login_page'),
    path('signup_page/', views.signup_view, name='signup_page'),
    path('logout/', views.custom_logout_view, name='logout_account'),

    path('admin/', admin.site.urls),

    path('student/', include('student.urls')),   
    path('teacher/', include('teacher.urls') ),

    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('games/<int:game_id>/play/', views.game_play, name='game_play'),
    path('session/<int:session_id>/question/', views.game_question, name='game_question'),
    path('results/<int:session_id>/', views.game_result, name='game_result'),
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('lesson/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('quizzes/', views.quiz_list, name='quiz_list'), 

    path('game/<int:game_id>/fraction_play/', views.fraction_game_play, name='fraction_game_play'),
    

    path('fraction_game/<int:game_id>/', views.fraction_game_play, name='fraction_game_play'),
    path('fraction_game/question/<int:session_id>/', views.fraction_game_question, name='fraction_game_question'),
    path('fraction_game/result/<int:session_id>/', views.fraction_game_result, name='fraction_game_result'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('objectives/', views.objectives_view, name='objectives'),
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('download-db-backup/', views.download_db_backup, name='download_db_backup'),
    path('restore_database/', views.restore_database, name='restore_database'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)