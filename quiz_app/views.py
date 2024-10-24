from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from teacher.models import Category, Game, GameSession, GameQuestion, GameChoice, Quiz,FractionGameQuestion, FractionGameSession
from .forms import LoginForm, SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

import random 

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
                    return redirect('home')  # Fallback redirect
                
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
    games = Game.objects.all()  # Fetch all games
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
        questions = list(GameQuestion.objects.filter(game=session.game).order_by('?'))
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
    games = Game.objects.all()

    multiple_choice_leaderboards = {}
    type_the_answer_leaderboards = {}

    for game in games:
        # Fetch all scores for multiple choice games
        mc_scores = (
            GameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Use F expression to keep original score
        )

        # Sort and get the top 5 by max score
        sorted_mc_scores = sorted(mc_scores, key=lambda x: x['max_score'], reverse=True)[:5]
        multiple_choice_leaderboards[game.name] = sorted_mc_scores

        # Fetch all scores for type the answer games
        ta_scores = (
            FractionGameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Use F expression to keep original score
        )

        # Sort and get the top 5 by max score
        sorted_ta_scores = sorted(ta_scores, key=lambda x: x['max_score'], reverse=True)[:5]
        type_the_answer_leaderboards[game.name] = sorted_ta_scores

    context = {
        'multiple_choice_leaderboards': multiple_choice_leaderboards,
        'type_the_answer_leaderboards': type_the_answer_leaderboards,
    }
    
    return render(request, 'home/leaderboard.html', context)