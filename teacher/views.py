from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Quiz, Question, Choice, Game, QuizAttempt, GameSession, FractionGameQuestion
from .forms import CategoryForm, QuizForm, EditQuizForm
from django.contrib import messages,  auth
from django.http import JsonResponse,  HttpResponseForbidden,  HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, IntegerField, Count
from django.db.models import F

def teacher_dashboard(request):
    # Define the custom order for games, if necessary for the teacher's dashboard
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

    # Initialize dictionaries for storing leaderboard-like data for the teacher's dashboard
    multiple_choice_data = {}
    type_the_answer_data = {}
    quiz_data = {}

    # Populate the data for multiple choice and type-the-answer games
    for game in games:
        # Multiple Choice Game Data
        mc_scores = (
            GameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Retain original score
        )
        sorted_mc_scores = sorted(mc_scores, key=lambda x: x['max_score'], reverse=True)[:10]
        multiple_choice_data[game.name] = sorted_mc_scores

        # Type the Answer Game Data
        ta_scores = (
            GameSession.objects
            .filter(game=game)
            .values('player_name')
            .annotate(max_score=F('score'))  # Retain original score
        )
        sorted_ta_scores = sorted(ta_scores, key=lambda x: x['max_score'], reverse=True)[:10]
        type_the_answer_data[game.name] = sorted_ta_scores

    # Populate quiz data
    for quiz in Quiz.objects.all():
        leaderboard = (
            QuizAttempt.objects
            .filter(quiz=quiz)
            .values('name')
            .annotate(max_score=F('score'))  # Retain original score
        )
        sorted_quiz_scores = sorted(leaderboard, key=lambda x: x['max_score'], reverse=True)[:10]
        quiz_data[quiz.title] = sorted_quiz_scores

    # Context data to be passed to the template
    context = {
        'multiple_choice_data': multiple_choice_data,
        'type_the_answer_data': type_the_answer_data,
        'quiz_data': quiz_data,
    }

    # Render the teacher's dashboard template with the provided context
    return render(request, 'teacher/teacher_dashboard.html', context)

def category_dashboard(request):
    categories = Category.objects.all()
    form = CategoryForm()  # If you want to add a new category, the form is still available
    return render(request, 'teacher/category_list.html', {'categories': categories, 'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CategoryForm()
    return render(request, 'teacher/add_category.html', {'form': form})

# Delete Category View
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')  # Redirect to the dashboard after deletion
    return render(request, 'teacher/delete_category.html', {'category': category})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'teacher/edit_category.html', {'form': form, 'category': category})

def quiz_list(request):
    user = request.user
    categories = Category.objects.prefetch_related('quizzes').all()
    return render(request, 'teacher/quiz_list.html', {'categories': categories})

def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz Created Successfully!')
            return redirect('quiz_list_teacher')
    else:
        form = QuizForm()
    return render(request, 'teacher/quiz_form.html', {'form': form})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all related questions

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'teacher/quiz_detail.html', context)


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Question.objects.create(quiz=quiz, text=text, category=quiz.category)
            messages.success(request, 'Question added successfully!')
        return redirect('quiz_detail', quiz_id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct', False)
        is_correct = True if is_correct == 'on' else False
        if text:
            Choice.objects.create(question=question, text=text, is_correct=is_correct, category=question.category)
            messages.success(request, 'Choice Successfully Added!')
        return redirect('quiz_detail', quiz_id=question.quiz.id)
    
    return render(request, 'quiz_detail.html', {'quiz': question.quiz})

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = EditQuizForm(request.POST, request.FILES, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully.')
            return redirect('quiz_detail', quiz_id=quiz.id)  # Redirect to quiz detail page after successful update
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'teacher/quiz_detail.html', {
        'form': form,
        'quiz': quiz
    })

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully.')
        return redirect('quiz_list_teacher')  # Redirect to the list of quizzes or another page

    return render(request, 'teacher/quiz_details.html', {'quiz': quiz})

def delete_choice(request):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        if not choice_id:
            return HttpResponseBadRequest('Missing choice_id')

        try:
            choice = Choice.objects.get(id=choice_id)
            choice.delete()
            return JsonResponse({'status': 'success'})
        except Choice.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Choice not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        question.delete()
        messages.success(request, 'Question deleted successfully.')
    return redirect('quiz_detail', quiz_id=question.quiz.id)


def type_the_answer(request):
    games = Game.objects.all()
    return render(request, 'teacher/type_the_answer.html', {'games': games})

def edit_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    questions = FractionGameQuestion.objects.filter(game=game)
    return render(request, 'teacher/edit_game.html', {'game': game, 'questions': questions})



def update_fraction_question(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        questions = FractionGameQuestion.objects.filter(game=game)
        
        for question in questions:
            text_key = f"question_text_{question.id}"
            numerator_key = f"numerator_{question.id}"
            denominator_key = f"denominator_{question.id}"
            
            # Check if the keys exist in the POST data
            if text_key in request.POST and numerator_key in request.POST and denominator_key in request.POST:
                try:
                    question_text = request.POST[text_key].strip()
                    correct_numerator = int(request.POST[numerator_key])
                    correct_denominator = int(request.POST[denominator_key])
                    
                    # Update the question fields
                    question.text = question_text
                    question.correct_numerator = correct_numerator
                    question.correct_denominator = correct_denominator
                    question.save()
                
                except ValueError:
                    return HttpResponseBadRequest("Invalid input values.")
        
        # Redirect back to the edit page after saving
        messages.success(request, 'Game Successfully Edited.')
        return redirect('edit_game', game_id=game.id)
    else:
        return HttpResponseBadRequest("Invalid request method.")
    

def multiple_choice_games(request):
    games = Game.objects.all()  # Fetch all games
    return render(request, 'teacher/multiple_choice_games.html', {'games': games})

def edit_multiple_choice(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # Filter questions that have at least one associated choice
    questions = game.questions.filter(game_choices__isnull=False).distinct()

    if request.method == "POST":
        for question in questions:
            # Update question text
            question_text = request.POST.get(f"question_text_{question.id}")
            if question_text:
                question.text = question_text
                question.save()

            # Update choices
            for choice in question.game_choices.all():
                choice_text = request.POST.get(f"choice_text_{choice.id}")
                is_correct = request.POST.get(f"choice_correct_{choice.id}", "off") == "on"
                if choice_text:
                    choice.text = choice_text
                    choice.is_correct = is_correct
                    choice.save()

        messages.success(request, "Game questions and choices updated successfully!")
        return redirect('edit_multiple_choice', game_id=game.id)

    return render(request, 'teacher/edit_multiple_choice.html', {
        'game': game,
        'questions': questions,
    })