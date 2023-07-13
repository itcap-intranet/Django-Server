from courses.models import QuizQuestion, Quiz, QuizAnswer
from courses.forms import QuizQuestionForm, QuizForm, QuizAnswerForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

# @login_required
# @permission_required('courses.add_quizquestion', raise_exception=True)
def quiz_question_create_view(request):
    print('create quiz question view')
    if request.method == 'POST':
        form2 = QuizQuestionForm(request.POST or None)

        if form2.is_valid():
            print(form2.cleaned_data)
            quiz_question = form2.save()
            form2 = QuizQuestionForm()
            form = QuizForm()
        else:
            print('form is not valid')
            print(form2.errors)
    else:
        form2 = QuizQuestionForm()
        form = QuizForm()

    data = {
        'form': form,
        'form2': form2,
        'quizzes': Quiz.objects.all(),
        'quiz_questions': get_quiz_questions(request),
    }

    return render(request, "settings/sections/quiz_settings.html", data)


# @login_required
# @permission_required('courses.view_quizquestion', raise_exception=True)
def get_quiz_questions(request):
    quiz_questions = QuizQuestion.objects.all()
    return quiz_questions


# @login_required
# @permission_required('courses.change_quizquestion', raise_exception=True)
def quiz_question_edit_view(request, quiz_question_id):
    quiz_question = get_object_or_404(QuizQuestion, id=quiz_question_id)
    quizzes = Quiz.objects.all()

    print('edit quiz question view')
    form = QuizQuestionForm(request.POST or None, instance=quiz_question)

    if form.is_valid():
        quiz_question = form.save()
        return HttpResponseRedirect('/settings/quizzes', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'quiz_question': quiz_question,
        'quizzes': quizzes,
    }
    return render(request, "settings/sections/forms/edit_quiz_question.html", context)


# @login_required
# @permission_required('courses.delete_quizquestion', raise_exception=True)
def quiz_question_delete_view(request, quiz_question_id):
    quiz_question = get_object_or_404(QuizQuestion, id=quiz_question_id)
    quiz_question.delete()
    return HttpResponseRedirect('/settings/quizzes')


# @login_required
# @permission_required('courses.view_quizquestion', raise_exception=True)
def manage_answers_view(request, quiz_question_id):
    quiz_question = get_object_or_404(QuizQuestion, id=quiz_question_id)
    quiz_answers = quiz_question.quizanswer_set.all()
    print(quiz_question.question)

    form = QuizAnswerForm()

    context = {
        'form': form,
        'quiz_question': quiz_question,
        'quiz_answers': quiz_answers
    }
    return render(request, "settings/sections/forms/manage_answers.html", context)

