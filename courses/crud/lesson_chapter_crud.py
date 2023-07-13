from courses.models import LessonChapter, Lesson
from courses.forms import LessonChapterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .quiz_crud import get_quiz_max_total_points
from django.contrib.auth.decorators import login_required, permission_required


# @login_required
# @permission_required('courses.add_lesson_chapter', raise_exception=True)
def lesson_chapter_create_view(request):
    print('create lesson chapter view')
    if request.method == 'POST':
        form = LessonChapterForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            author = form.save()
            form = LessonChapterForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = LessonChapterForm()

    data = {
        'form': form,
        'lesson_chapters': get_lesson_chapters(request),
    }

    return render(request, "settings/sections/lesson_chapter_settings.html", data)


# @login_required
# @permission_required('courses.view_lesson_chapter', raise_exception=True)
def get_lesson_chapters(request):
    lesson_chapters = LessonChapter.objects.all()
    return lesson_chapters


# @login_required
# @permission_required('courses.change_lessonchapter', raise_exception=True)
def lesson_chapter_edit_view(request, lesson_chapter_id):
    lesson_chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)
    lessons = Lesson.objects.all()

    print('edit lesson chapter view')
    form = LessonChapterForm(request.POST or None, instance=lesson_chapter)

    if form.is_valid():
        lesson_chapter = form.save()
        return HttpResponseRedirect('/settings/lesson_chapters', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'lesson_chapter': lesson_chapter,
        'lessons': lessons,
    }
    return render(request, "settings/sections/forms/edit_lesson_chapter.html", context)


# @login_required
# @permission_required('courses.delete_lessonchapter', raise_exception=True)
def lesson_chapter_delete_view(request, lesson_chapter_id):
    lesson_chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)
    lesson_chapter.delete()
    return HttpResponseRedirect('/settings/lesson_chapters')

# @login_required
# @permission_required('courses.view_lessonchapter', raise_exception=True)
def get_lesson_chapter_max_total_points(request, lesson_chapter_id):
    lesson_chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)
    max_total_points = 0

    # later add video points here

    quizzes = lesson_chapter.quiz_set.all()
    for quiz in quizzes:
        max_total_points += get_quiz_max_total_points(request, quiz.id)

    assignments = lesson_chapter.assignment_set.all()
    for assignment in assignments:
        max_total_points += assignment.points

    return max_total_points
