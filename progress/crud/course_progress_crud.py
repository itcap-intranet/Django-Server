from progress.models import UserProgress, UserCourseProgress, UserLessonProgress
from courses.models import Course
from courses.crud.course_crud import get_course_max_total_points
from courses.crud.lesson_crud import get_lesson_max_total_points
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

# @login_required
# @permission_required('progress.view_usercourseprogress', raise_exception=True)
def is_course_completed(request, course_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    course = get_object_or_404(Course, id=course_id)

    try:
        course_progress = UserCourseProgress.objects.get(user_progress=user_progress, course=course)
        return course_progress.completed
    except UserCourseProgress.DoesNotExist:
        return False

# @login_required
# @permission_required('progress.view_usercourseprogress', raise_exception=True)
def is_course_started(request, course_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    course = get_object_or_404(Course, id=course_id)

    try:
        course_progress = UserCourseProgress.objects.get(user_progress=user_progress, course=course)
        return course_progress.progress > 0
    except UserCourseProgress.DoesNotExist:
        return 0

# @login_required
# @permission_required('progress.view_usercourseprogress', raise_exception=True)
def get_course_progress(request, course_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    course = get_object_or_404(Course, id=course_id)

    try:
        course_progress = UserCourseProgress.objects.get(user_progress=user_progress, course=course)
        return course_progress.progress
    except UserCourseProgress.DoesNotExist:
        return 0

# @login_required
# @permission_required('progress.view_usercourseprogress', raise_exception=True)
def check_course_completed(request, course_id):
    print("check_course_completed")
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    course = get_object_or_404(Course, id=course_id)
    max_total_points = get_course_max_total_points(request, course_id)

    user_total_points = 0
    lessons = course.lesson_set.all()
    for lesson in lessons:
        user_lesson_progresses = UserLessonProgress.objects.filter(user_progress=user_progress, lesson=lesson)
        for user_lesson_progress in user_lesson_progresses:
            if user_lesson_progress.completed:
                lesson = user_lesson_progress.lesson
                points_for_lesson = get_lesson_max_total_points(request, lesson.id)
                user_total_points += points_for_lesson

    if user_total_points == max_total_points:
        return True
    else:
        return False

# @login_required
# @permission_required('progress.change_usercourseprogress', raise_exception=True)
def mark_course_as_completed(request, course_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    course = get_object_or_404(Course, id=course_id)

    course_progress, created = UserCourseProgress.objects.get_or_create(user_progress=user_progress, course=course)
    course_progress.progress = 100
    course_progress.completed = True
    course_progress.save()

