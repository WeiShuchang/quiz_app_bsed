from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Quiz, Question, Choice, Game, QuizAttempt, GameSession
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

