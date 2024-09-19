from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Quiz, Question, Choice, Class
from .forms import CategoryForm, QuizForm, EditQuizForm, ClassForm
from django.contrib import messages,  auth
from django.http import JsonResponse,  HttpResponseForbidden,  HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def teacher_dashboard(request):
    return render(request, "teacher/teacher_dashboard.html")

def category_dashboard(request):
    # Get the logged-in user
    user = request.user
    
    # Filter classes where the logged-in user is the teacher
    classes = Class.objects.filter(teacher=user)
    
    # Filter categories where the class_assigned's teacher matches the logged-in user
    categories = Category.objects.filter(class_assigned__teacher=user)

    form = CategoryForm()  # If you want to add a new category, the form is still available

    return render(request, 'teacher/category_list.html', {'classes': classes, 'categories': categories, 'form': form})

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
    return render(request, 'seller/delete_category.html', {'category': category})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    classes = Class.objects.all()  # Fetch all classes for the dropdown

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'teacher/edit_category.html', {'form': form, 'category': category, 'classes': classes})

def quiz_list(request):
    # Get the logged-in user
    user = request.user

    # Filter classes and categories by the logged-in user (teacher)
    classes = Class.objects.filter(teacher=user).prefetch_related('categories__quizzes')  # Optimize queries
    categories = Category.objects.filter(class_assigned__teacher=user)

    return render(request, 'teacher/quiz_list.html', {'classes': classes, 'categories': categories})

def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz Created Successfully!')
            return redirect('quiz_list')
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
        return redirect('quiz_list')  # Redirect to the list of quizzes or another page

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

@login_required
def class_dashboard(request):
    # Get the logged-in user
    user = request.user

    # Filter classes by the logged-in user (teacher)
    classes = Class.objects.filter(teacher=user)

    context = {
        'classes': classes,
    }
    return render(request, 'teacher/class_dashboard.html', context)

@login_required
def edit_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('class_dashboard')
        else:
            messages.error(request, 'Error updating class. Please check the details.')
    else:
        form = ClassForm(instance=class_instance)

    context = {
        'form': form,
        'class_instance': class_instance,
    }
    return render(request, 'teacher/class_form.html', context)

@login_required
def delete_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_instance.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('class_dashboard')

    context = {
        'class_instance': class_instance,
    }
    return render(request, 'teacher/class_confirm_delete.html', context)


@login_required
def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = request.user  # Automatically set the teacher to the logged-in user
            new_class.save()
            messages.success(request, 'Class created successfully.')
            return redirect('class_dashboard')  # Redirect to the class dashboard after successful creation
        else:
            messages.error(request, 'Error creating class. Please check the details.')
    else:
        form = ClassForm()
    
    context = {
        'form': form,
    }
    return render(request, 'teacher/class_dashboard.html', context)

def class_quizzes_view(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)
    categories = classroom.categories.all()  # Get all categories linked to the class

    context = {
        'classroom': classroom,
        'categories': categories,
    }
    return render(request, 'student/class_detail.html', context)
