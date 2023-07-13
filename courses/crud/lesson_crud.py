from courses.models import Lesson, Course
from courses.forms import LessonForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .lesson_chapter_crud import get_lesson_chapter_max_total_points
from django.contrib.auth.decorators import login_required, permission_required

# @login_required
# @permission_required('courses.add_lesson', raise_exception=True)
def lesson_create_view(request):
    print('create lesson view')
    if request.method == 'POST':
        form = LessonForm(request.POST or None)

        if form.is_valid():
            print(form.cleaned_data)
            lesson = form.save()
            form = LessonForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = LessonForm()

    data = {
        'form': form,
        'lessons': get_lessons(request),
    }

    return render(request, "settings/sections/lesson_settings.html", data)


# @login_required
# @permission_required('courses.view_lesson', raise_exception=True)
def get_lessons(request):
    lessons = Lesson.objects.all()
    return lessons


# @login_required
# @permission_required('courses.change_lesson', raise_exception=True)
def lesson_edit_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    courses = Course.objects.all()

    print('edit lesson view')
    form = LessonForm(request.POST or None, instance=lesson)

    if form.is_valid():
        lesson = form.save()
        return HttpResponseRedirect('/settings/lessons', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'lesson': lesson,
        'courses': courses,
    }
    return render(request, "settings/sections/forms/edit_lesson.html", context)


# @login_required
# @permission_required('courses.delete_lesson', raise_exception=True)
def lesson_delete_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return HttpResponseRedirect('/settings/lessons')

# @login_required
# @permission_required('courses.view_lesson', raise_exception=True)
def get_lesson_max_total_points(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    max_total_points = 0

    lesson_chapters = lesson.lessonchapter_set.all()

    for lesson_chapter in lesson_chapters:
        max_total_points += get_lesson_chapter_max_total_points(request, lesson_chapter.id)

    return max_total_points
