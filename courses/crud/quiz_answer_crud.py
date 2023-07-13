from courses.models import QuizAnswer, QuizQuestion
from courses.forms import QuizAnswerForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, permission_required


# @login_required
# @permission_required('courses.add_quizanswer', raise_exception=True)
def quiz_answer_create_view(request, quiz_question_id):
    print('create quiz answer view')


    if request.method == 'POST':
        form = QuizAnswerForm(request.POST or None)

        if form.is_valid():
            print('form is valid')
            print(form.cleaned_data)
            quiz_answer = form.save()
            form = QuizAnswerForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = QuizAnswerForm()

    quiz_question = get_object_or_404(QuizQuestion, id=quiz_question_id)
    quiz_answers = quiz_question.quizanswer_set.all()

    data = {
        'form': form,
        'quiz_question': quiz_question,
        'quiz_answers': quiz_answers,
    }

    return render(request, "settings/sections/forms/manage_answers.html", data)


# @login_required
# @permission_required('courses.view_quizanswer', raise_exception=True)
def get_quiz_answers(request):
    quiz_answers = QuizAnswer.objects.all()
    return quiz_answers


# @login_required
# @permission_required('courses.delete_quizanswer', raise_exception=True)
def quiz_answer_delete_view(request, quiz_answer_id):
    quiz_answer = get_object_or_404(QuizAnswer, id=quiz_answer_id)
    print(quiz_answer)
    quiz_question = quiz_answer.question
    quiz_answer.delete()

    quiz_answers = quiz_question.quizanswer_set.all()
    context = {
        'quiz_question': quiz_question,
        'quiz_answers': quiz_answers
    }

    return HttpResponseRedirect('/course/manage_answers/' + str(quiz_question.id), context)

# @login_required
# @permission_required('courses.view_quizanswer', raise_exception=True)
def get_correct_answer_by_question_id(request, question_id):
    answers = QuizAnswer.objects.filter(question_id=question_id)
    for answer in answers:
        if answer.is_correct:
            return answer.id