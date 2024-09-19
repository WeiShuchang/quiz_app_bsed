from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages,  auth
from teacher.models import Class, Class, QuizAttempt, Choice, Quiz
from .models import StudentClass
from .forms import JoinClassForm
from django.http import HttpResponseRedirect


@login_required
def student_dashboard(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                # Check if the class with the given code exists
                classroom = Class.objects.get(code=code)
                
                # Check if the student is already enrolled
                if StudentClass.objects.filter(student=request.user, classroom=classroom).exists():
                    messages.warning(request, "You are already enrolled in this class.")
                else:
                    # Enroll the student in the class
                    StudentClass.objects.create(student=request.user, classroom=classroom)
                    messages.success(request, "Successfully joined the class!")
                    
                return redirect('student_dashboard')
            except Class.DoesNotExist:
                messages.error(request, "Invalid class code. Please try again.")
    else:
        form = JoinClassForm()

    # Query enrolled classes for the logged-in user
    enrolled_classes = StudentClass.objects.filter(student=request.user)

    # Render the student dashboard template with the form and enrolled classes
    return render(request, 'student/student_dashboard.html', {'form': form, 'enrolled_classes': enrolled_classes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    context = {
        'quiz': quiz
    }
    return render(request, 'student/quiz_detail.html', context)


@login_required
def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.id}')
            if selected_choice:
                choice = get_object_or_404(Choice, id=selected_choice)
                if choice.is_correct:
                    score += 1
        
        # Save the attempt
        QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            category=quiz.category
        )
        
        # Redirect to the results or summary page
        return redirect('quiz_result', quiz_id=quiz_id)

    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'student/quiz_attempt.html', context)

@login_required
def quiz_result(request, quiz_id):
    attempt = get_object_or_404(QuizAttempt, quiz_id=quiz_id, user=request.user)
    
    context = {
        'attempt': attempt
    }
    return render(request, 'student/quiz_result.html', context)
