from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from teacher.models import Category, Game, GameSession, GameQuestion, GameChoice, Quiz,FractionGameQuestion, FractionGameSession
from .forms import LoginForm, SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Case, When, IntegerField, Count
from django.conf import settings
from django.http import FileResponse
import random 
from django.contrib.auth.decorators import login_required
from datetime import datetime
import os
import shutil
from django.http import HttpResponse
import sqlite3

def home(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "home/landing_page.html", context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Check the user's role and redirect accordingly
                if user.userprofile.role == 'teacher':
                    return redirect('teacher_dashboard')  # Redirect to teacher dashboard
                elif user.userprofile.role == 'student':
                    return redirect('student_dashboard')  # Redirect to student dashboard
                else:
                    return redirect('login_page')  # Fallback redirect
                
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'home/login_page.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically assign the role of 'student' upon signup
            user.userprofile.role = 'student'
            user.userprofile.save()

            # Authenticate and log in the user
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Account created and logged in successfully!')
                return redirect('student_dashboard')  # Redirect to student dashboard after successful signup
    else:
        form = SignupForm()
    
    return render(request, 'home/signup_page.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('landing')  # Replace 'landing' with your landing page URL name

def game_list(request):
    # Define the custom order
    order = [
        "Simplifying Fractions Game",
        "Mixed & Improper Fractions Game",
        "Adding Fractions Game",
        "Subtracting Fractions Game",
        "Multiplying Fractions Game",
        "Dividing Fractions Game"
    ]

    # Annotate each game with a specific order based on the title
    games = Game.objects.annotate(
        custom_order=Case(
            *[When(name=title, then=index) for index, title in enumerate(order)],
            output_field=IntegerField()
        )
    ).order_by("custom_order")

    return render(request, 'home/game_list.html', {'games': games})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'home/game_detail.html', {'game': game})

def game_play(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        # Start a new game session
        session = GameSession.objects.create(player_name=request.POST.get('user_name'), game=game)
        request.session['session_id'] = session.id
        return redirect('game_question', session.id)

    return render(request, 'home/game_play.html', {'game': game})

def game_question(request, session_id):
    session = get_object_or_404(GameSession, id=session_id)

    # Fetch the question list from session if it's a returning game
    if 'question_list' not in request.session or session.current_question == 0:
        # Get questions that have at least one GameChoice
        questions = list(GameQuestion.objects.filter(game=session.game)
                         .annotate(choice_count=Count('game_choices'))
                         .filter(choice_count__gt=0)
                         .order_by('?'))
        request.session['question_list'] = [q.id for q in questions]
    else:
        question_ids = request.session['question_list']
        questions = GameQuestion.objects.filter(id__in=question_ids)

    # Handle POST request (user submits an answer)
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        question = questions[session.current_question]

        # Store the selected answer in the session
        session.selected_answers[str(question.id)] = selected_choice_id
        
        # Check the correctness of the selected choice
        correct_choice = GameChoice.objects.filter(question=question, is_correct=True).first()
        if correct_choice and str(selected_choice_id) == str(correct_choice.id):
            session.score += 1

        # Update the current question index
        session.current_question += 1
        session.save()  # Save the session after updating

        # Debug print to check selected answers
        print(f"Selected Answers: {session.selected_answers}")

        if session.current_question >= session.game.total_questions:
            del request.session['question_list']  # Clear question list after game ends
            return redirect('game_result', session.id)

        return redirect('game_question', session.id)

    # Get the current question
    question = questions[session.current_question]
    choices = list(question.game_choices.all())
    random.shuffle(choices)  # Shuffle the choices

    context = {
        'session': session,
        'question': question,
        'choices': choices,
        'current_question_number': session.current_question + 1,
        'time_left': session.game.duration  # Fetching game duration from session's related game
    }

    return render(request, 'home/game_question.html', context)

def game_result(request, session_id):
    session = get_object_or_404(GameSession, id=session_id)
    return render(request, 'home/game_result.html', {'session': session})

def lessons_list(request):
    return render(request, "home/lessons_list.html")

def lesson_detail(request, lesson_slug):
    template_name = f"home/lessons/{lesson_slug}.html"
    return render(request, template_name)

def quiz_list(request):
    # Query all quizzes
    quizzes = Quiz.objects.all()
    return render(request, 'home/quiz_list.html', {'quizzes': quizzes})

def fraction_game_question(request, session_id):
    session = get_object_or_404(FractionGameSession, id=session_id)

    # Initialize selected_answers in session if it doesn't exist
    if 'selected_answers' not in session.__dict__:
        session.selected_answers = {}

    # Fetch the question list from session if it's a returning game
    if 'question_list' not in request.session or session.current_question == 0:
        questions = list(FractionGameQuestion.objects.filter(game=session.game).order_by('?'))
        request.session['question_list'] = [q.id for q in questions]
    else:
        question_ids = request.session['question_list']
        questions = FractionGameQuestion.objects.filter(id__in=question_ids)

    # Handle POST request (user submits an answer)
    if request.method == 'POST':
        numerator = request.POST.get('numerator')
        denominator = request.POST.get('denominator')
        question = questions[session.current_question]

        # Store the selected answer in the session
        session.selected_answers[str(question.id)] = {'numerator': numerator, 'denominator': denominator}

        # Check the correctness of the answer without affecting scoring
        if numerator == str(question.correct_numerator) and denominator == str(question.correct_denominator):
            session.score += 1

        # Update the current question index
        session.current_question += 1
        session.save()  # Save the session after updating

        if session.current_question >= session.game.total_questions:
            del request.session['question_list']  # Clear question list after game ends
            return redirect('fraction_game_result', session.id)

        return redirect('fraction_game_question', session.id)

    # Get the current question
    question = questions[session.current_question]
    total_questions = session.game.total_questions

    context = {
        'session': session,
        'question': question,
        'total_questions': total_questions,
        'current_question_number': session.current_question + 1,
        'time_left': session.game.duration  # Fetching game duration from session's related game
    }

    return render(request, 'home/fraction_game_question.html', context)


def fraction_game_play(request, game_id):
    # Retrieve the game object
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        # Create a new game session for the given game
        session = FractionGameSession.objects.create(
            player_name=request.POST.get('user_name'), 
            game=game
        )
        
        # Initialize session variables
        request.session['question_list'] = []
        request.session['selected_answers'] = {}
        request.session['current_question'] = 0
        request.session['score'] = 0
        request.session['time_left'] = game.duration  # Set the time left to game duration
        
        # Save session instance after initialization
        session.save()
        
        # Redirect to the first question
        return redirect('fraction_game_question', session.id)

    return render(request, 'home/fraction_game_play.html', {'game': game})

def fraction_game_result(request, session_id):
    session = get_object_or_404(FractionGameSession, id=session_id)

    # Calculate the percentage score if you want to show that as well
    total_questions = session.game.total_questions
    percentage_score = (session.score / total_questions) * 100 if total_questions > 0 else 0

    context = {
        'session': session,
        'percentage_score': percentage_score,
        'total_questions': total_questions,
    }

    return render(request, 'home/fraction_game_result.html', context)

def leaderboard_view(request):
    # Define the custom order
    order = [
        "Simplifying Fractions Game",
        "Mixed & Improper Fractions Game",
        "Adding Fractions Game",
        "Subtracting Fractions Game",
        "Multiplying Fractions Game",
        "Dividing Fractions Game"
    ]

    # Annotate games with a custom order field
    games = Game.objects.annotate(
        custom_order=Case(
            *[When(name=title, then=index) for index, title in enumerate(order)],
            output_field=IntegerField()
        )
    ).order_by("custom_order")

    # Initialize leaderboard dictionaries
    multiple_choice_leaderboards = {}
    type_the_answer_leaderboards = {}

    # Populate leaderboards in the custom order
    for game in games:
        # Multiple Choice Leaderboard
        mc_scores = (
            GameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Retain original score
        )
        sorted_mc_scores = sorted(mc_scores, key=lambda x: x['max_score'], reverse=True)[:10]
        multiple_choice_leaderboards[game.name] = sorted_mc_scores

        # Type the Answer Leaderboard
        ta_scores = (
            FractionGameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Retain original score
        )
        sorted_ta_scores = sorted(ta_scores, key=lambda x: x['max_score'], reverse=True)[:10]
        type_the_answer_leaderboards[game.name] = sorted_ta_scores

    context = {
        'multiple_choice_leaderboards': multiple_choice_leaderboards,
        'type_the_answer_leaderboards': type_the_answer_leaderboards,
    }
    
    return render(request, 'home/leaderboard.html', context)

def objectives_view(request):
    return render (request, "home/objectives_page.html")

def aboutus_view(request):
    return render (request, "home/aboutus_page.html")


 
def download_db_backup(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if os.path.exists(db_path):
        # Format the date in 'YYYY-MM-DD' format
        date_str = datetime.now().strftime("%B %d, %Y")
        filename = f"db_backup_{date_str}.sqlite3"
        
        response = FileResponse(open(db_path, 'rb'), content_type='application/x-sqlite3')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("Database file not found.", status=404)



def restore_database(request):
    if request.method == 'POST' and request.FILES.get('db_file'):
        db_file = request.FILES['db_file']
        
        # Confirm file type is correct
        if not db_file.name.endswith('.sqlite3'):
            messages.error(request, "Please upload a valid SQLite3 database file (.sqlite3).")
            return redirect('restore_database')

        # Paths for backup and current database
        backup_path = os.path.join(settings.BASE_DIR, 'db_backup.sqlite3')
        current_db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        temp_db_path = os.path.join(settings.BASE_DIR, 'temp_uploaded_db.sqlite3')

        try:
            # Save uploaded file temporarily
            with open(temp_db_path, 'wb+') as temp_db:
                for chunk in db_file.chunks():
                    temp_db.write(chunk)
            
            # Check table structure in current and uploaded databases
            def get_table_names(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = {table[0] for table in cursor.fetchall()}
                conn.close()
                return tables

            current_tables = get_table_names(current_db_path)
            uploaded_tables = get_table_names(temp_db_path)
            
            # Verify table structure
            if current_tables != uploaded_tables:
                messages.error(request, "The uploaded database does not have the same structure as the current database.")
                os.remove(temp_db_path)  # Remove temporary uploaded database file
                return redirect('restore_database')

            # Backup current database
            if os.path.exists(current_db_path):
                shutil.copy(current_db_path, backup_path)
            
            # Replace current database with uploaded file
            shutil.move(temp_db_path, current_db_path)
            messages.success(request, "Database restored successfully!")

        except Exception as e:
            # Restore from backup if something goes wrong
            if os.path.exists(backup_path):
                shutil.copy(backup_path, current_db_path)

            messages.error(request, f"An error occurred while restoring: {str(e)}")
            return redirect('restore_database')

        return redirect('restore_database')

    return render(request, 'teacher/restore_database.html')