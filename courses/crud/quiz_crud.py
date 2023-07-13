from courses.models import Quiz, QuizAnswer, QuizQuestion, LessonChapter
from courses.forms import QuizForm, QuizQuestionForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from courses.crud.quiz_answer_crud import get_correct_answer_by_question_id

# @login_required
# @permission_required('courses.add_quiz', raise_exception=True)
def quiz_create_view(request):
    print('create quiz view')
    if request.method == 'POST':
        form = QuizForm(request.POST or None)

        if form.is_valid():
            print(form.cleaned_data)
            quiz = form.save()
            form = QuizForm()
            form2 = QuizQuestionForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = QuizForm()
        form2 = QuizQuestionForm()

    data = {
        'form': form,
        'form2': form2,
        'quizzes': get_quizzes(request),
        'quiz_questions': QuizQuestion.objects.all(),
    }

    return render(request, "settings/sections/quiz_settings.html", data)


# @login_required
# @permission_required('courses.view_quiz', raise_exception=True)
def get_quizzes(request):
    quizzes = Quiz.objects.all()
    return quizzes


# @login_required
# @permission_required('courses.change_quiz', raise_exception=True)
def quiz_edit_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_chapters = LessonChapter.objects.filter(type='Quiz')

    print('edit quiz view')
    form = QuizForm(request.POST or None, instance=quiz)

    if form.is_valid():
        quiz = form.save()
        return HttpResponseRedirect('/settings/quizzes', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'quiz': quiz,
        'quiz_chapters': quiz_chapters,
    }
    return render(request, "settings/sections/forms/edit_quiz.html", context)


# @login_required
# @permission_required('courses.delete_quiz', raise_exception=True)
def quiz_delete_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return HttpResponseRedirect('/settings/quizzes')





# @login_required
# @permission_required('courses.view_quiz', raise_exception=True)
def get_quiz_max_total_points(request, quiz_id):
    quiz_questions = QuizQuestion.objects.filter(quiz_id=quiz_id)
    total_points = 0
    for question in quiz_questions:
        total_points += question.points
    return total_points


# @login_required
# @permission_required('courses.view_quiz', raise_exception=True)
def check_quiz_answers(request, quiz_id, my_answers):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_questions = QuizQuestion.objects.filter(quiz_id=quiz_id)

    total_points = 0

    for question in quiz_questions:
        correct_answer_id = int(get_correct_answer_by_question_id(request, question.id))
        my_answer_id = int(my_answers['radios-' + str(question.id)])
        if correct_answer_id == my_answer_id:
            total_points += question.points
            print("correct")
        else:
            total_points += 0
            print("incorrect")
            print("correct answer: " + str(correct_answer_id))
            print("my answer: " + str(my_answer_id))

    print("total points: " + str(total_points))
    return total_points
