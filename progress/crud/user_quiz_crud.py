from courses.models import Quiz
from progress.forms import QuizSubmissionForm
from django.http import HttpResponseRedirect
from courses.crud.quiz_crud import check_quiz_answers, get_quiz_max_total_points
from progress.models import UserQuizSubmission
from progress.crud.user_progress_crud import get_user_progress_by_user
from progress.crud.user_activity_crud import record_activity
from progress.crud.chapter_progress_crud import get_chapter_progress, mark_chapter_as_completed
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect

# @login_required
# @permission_required('progress.add_userquizsubmission', raise_exception=True)
def submit_quiz_view(request, quiz_id):
    print("TEST")
    print(quiz_id)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    lesson = quiz.chapter.lesson
    chapter = quiz.chapter

    print(quiz)
    print(lesson)
    print(chapter)

    total_points = 0

    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print('form is valid')
            # quiz_id = form.cleaned_data.get('quiz_id')
            # quiz = get_object_or_404(Quiz, id=quiz_id)
            # print(quiz_id)

            my_answers = form.form_data

            total_points = check_quiz_answers(request, quiz_id, my_answers)
            max_total_points = get_quiz_max_total_points(request, quiz_id)

            print('total_points: '+ str(total_points))
            print('max_total_points: '+ str(max_total_points))

            if (total_points == max_total_points):

                user_progress = get_user_progress_by_user(request, request.user)
                user_quiz_submission = UserQuizSubmission.objects.create(
                    quiz_id=quiz,
                    user_progress_id=user_progress,
                    total_points=total_points,
                    passed=True
                )
                user_quiz_submission.save()

                chapter_progress = get_chapter_progress(request, quiz.chapter.id)
                if chapter_progress.completed == False:
                    record_activity(request, quiz.chapter.id, total_points)
                    # @TODO
                    # update_lesson_progress(request, lesson.id, total_points)
                    # update_course_progress(request, quiz.chapter.id, total_points)

                    mark_chapter_as_completed(request, quiz.chapter.id)



            form = QuizSubmissionForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = QuizSubmissionForm()

    context = {
        'total_points': total_points,
        'quiz': quiz,
        'form': form,
        'chapter': chapter,
        'lesson': lesson,
        'lesson_chapters': lesson.lessonchapter_set.all(),
    }


    return redirect('courses:lesson-chapter-details', lesson_id=lesson.id, chapter_id=chapter.id)


    # return HttpResponseRedirect('/course/lesson/' + str(lesson.id) + "/chapter/" + str(quiz.chapter.id), context)


# @login_required
# @permission_required('progress.view_userquizsubmission', raise_exception=True)
def get_user_quizzes(request):
    user = request.user
    user_progress = get_user_progress_by_user(request, user)
    user_quizzes = UserQuizSubmission.objects.filter(user_progress_id=user_progress)
    return user_quizzes


# @login_required
# @permission_required('progress.delete_userquizsubmission', raise_exception=True)
def user_quiz_delete_view(request, user_quiz_id):
    user_quiz = get_object_or_404(UserQuizSubmission, id=user_quiz_id)
    user_quiz.delete()
    return HttpResponseRedirect('/progress/my_progress/')
