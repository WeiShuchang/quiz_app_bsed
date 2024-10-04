from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages,  auth
from teacher.models import QuizAttempt, Choice, Quiz
from .forms import JoinClassForm
from django.http import HttpResponseRedirect

@login_required
def student_dashboard(request):
    quizzes = Quiz.objects.all()  # Fetch all quizzes or you can filter them if needed
    return render(request, 'student/student_dashboard.html', {'quizzes': quizzes})

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

