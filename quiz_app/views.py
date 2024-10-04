from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from teacher.models import Category, Game, GameSession, GameQuestion, GameChoice, Quiz
from .forms import LoginForm, SignupForm

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
    questions = GameQuestion.objects.filter(game=session.game).order_by('?')

    if request.method == 'POST':
        selected_choice = request.POST.get('choice')
        correct = GameChoice.objects.filter(question=questions[session.current_question], is_correct=True).first()
        if selected_choice == correct.text:
            session.score += 1
            session.save()
        session.current_question += 1
        session.save()
        if session.current_question >= session.game.total_questions:
            return redirect('game_result', session.id)

        return redirect('game_question', session.id)

    question = questions[session.current_question]
    choices = question.game_choices.all()

    # Pass the current question number + 1 to the template
    context = {
        'session': session,
        'question': question,
        'choices': choices,
        'current_question_number': session.current_question + 1
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