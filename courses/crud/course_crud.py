from courses.models import Course, Author
from courses.forms import CourseForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .lesson_crud import get_lesson_max_total_points
from django.contrib.auth.decorators import login_required, permission_required



# @login_required
# @permission_required('courses.add_course', raise_exception=True)
def course_create_view(request):
    print('create course view')
    if request.method == 'POST':
        form = CourseForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print(form.cleaned_data)
            course = form.save()
            form = CourseForm()
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = CourseForm()

    data = {
        'form': form,
        'courses': get_courses(request),
    }

    return render(request, "settings/sections/course_settings.html", data)


# @login_required
# @permission_required('courses.view_course', raise_exception=True)
def get_courses(request):
    courses = Course.objects.all()
    return courses


# @login_required
# @permission_required('courses.change_course', raise_exception=True)
def course_edit_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    authors = Author.objects.all()

    print('edit course view')
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)

    if form.is_valid():
        course = form.save()
        return HttpResponseRedirect('/settings/courses', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'course': course,
        'authors': authors,
    }
    return render(request, "settings/sections/forms/edit_course.html", context)


# @login_required
# @permission_required('courses.delete_course', raise_exception=True)
def course_delete_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return HttpResponseRedirect('/settings/courses')

# @login_required
# @permission_required('courses.view_course', raise_exception=True)
def get_course_max_total_points(request, course_id):
    course = Course.objects.get(id=course_id)
    max_total_points = 0

    lessons = course.lesson_set.all()

    for lesson in lessons:
        max_total_points += get_lesson_max_total_points(request, lesson.id)

    return max_total_points
