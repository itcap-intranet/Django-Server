from django.shortcuts import render
from .models import UserProgress, UserCourseProgress, UserLessonProgress, UserLessonChapterProgress
from django.views import generic
from progress.crud import user_assignment_crud, user_quiz_crud, user_progress_crud, course_progress_crud, \
    lesson_progress_crud, chapter_progress_crud, user_activity_crud
from django.contrib.auth.decorators import login_required


# @login_required
def get_my_progress(request):
    context = {
        'user_assignments': user_assignment_crud.get_user_assignments(request),
        'user_quizzes': user_quiz_crud.get_user_quizzes(request),
    }
    return render(request, "progress/my_progress.html", context)


# @login_required
def leaderboard(request):
    context = {
        'user_results': user_progress_crud.get_user_results_for_leaderboard(request),
    }
    return render(request, "progress/leaderboard.html", context)


# @login_required
def get_user_stats(request):
    daily_points = user_progress_crud.get_daily_points(request, request.user)
    total_points = user_progress_crud.get_total_points(request, request.user)
    completed_lessons_num = user_progress_crud.get_completed_lessons_num(request)
    completed_courses_num = user_progress_crud.get_completed_courses_num(request)

    user_stats = {
        'daily_points': daily_points,
        'total_points': total_points,
        'completed_lessons_num': completed_lessons_num,
        'completed_courses_num': completed_courses_num,
    }
    return user_stats


# @login_required
def get_course_stats(request, course_id):
    course_progress = course_progress_crud.get_course_progress(request, course_id)
    course_completed = course_progress_crud.is_course_completed(request, course_id)
    course_started = course_progress_crud.is_course_started(request, course_id)

    course_stats = {
        'course_progress': course_progress,
        'is_completed': course_completed,
        'is_started': course_started,
    }

    return course_stats


# @login_required
def get_lesson_stats(request, lesson_id):
    lesson_progress = lesson_progress_crud.get_lesson_progress(request, lesson_id)
    lesson_completed = lesson_progress_crud.is_lesson_completed(request, lesson_id)
    lesson_started = lesson_progress_crud.is_lesson_started(request, lesson_id)

    lesson_stats = {
        'lesson_progress': lesson_progress,
        'is_completed': lesson_completed,
        'is_started': lesson_started,
    }

    return lesson_stats


# @login_required
def get_chapter_stats(request, chapter_id):
    chapter_progress = chapter_progress_crud.get_chapter_progress_percentage(request, chapter_id)
    chapter_completed = chapter_progress_crud.is_chapter_completed(request, chapter_id)
    chapter_started = chapter_progress_crud.is_chapter_started(request, chapter_id)

    chapter_stats = {
        'chapter_progress': chapter_progress,
        'is_completed': chapter_completed,
        'is_started': chapter_started,
    }

    return chapter_stats


# @login_required
def get_top_learners_this_week(request):
    top_learners = user_progress_crud.get_top_learners_this_week(request)
    return top_learners


# @login_required
def get_course_activity_list(request):
    course_activity_list = user_activity_crud.get_course_activity_list(request)
    return course_activity_list

# @login_required
def get_active_courses(request):
    active_courses = user_progress_crud.get_active_courses(request)
    return active_courses