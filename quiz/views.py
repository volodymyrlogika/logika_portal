from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, AnswerOption, UserAnswer

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # отримаємо всі питання цього тесту
    questions = quiz.Запитання.all()  

    if request.method == 'POST':
        # видаляємо попередні відповіді користувача на цей тест
        UserAnswer.objects.filter(user=request.user, survey=quiz).delete()

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            text_answer = request.POST.get(f"text_{question.id}")

            if selected_option_id:
                option = AnswerOption.objects.get(id=selected_option_id)
                UserAnswer.objects.create(
                    user=request.user,
                    survey=quiz,
                    question=question,
                    selected_option=option
                )
            elif text_answer:
                UserAnswer.objects.create(
                    user=request.user,
                    survey=quiz,
                    question=question,
                    text_answer=text_answer
                )

        return redirect("quiz_result", quiz_id=quiz.id)

    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "questions": questions})


@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = UserAnswer.objects.filter(user=request.user, survey=quiz)

    return render(request, "quiz/result.html", {"quiz": quiz, "answers": answers})