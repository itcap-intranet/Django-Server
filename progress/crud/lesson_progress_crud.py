from progress.models import UserProgress, UserLessonProgress, UserLessonChapterProgress
from courses.models import Lesson
from courses.crud.lesson_crud import get_lesson_max_total_points
from progress.crud.course_progress_crud import check_course_completed, mark_course_as_completed
from courses.crud.lesson_chapter_crud import get_lesson_chapter_max_total_points
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

# @login_required
# @permission_required('progress.view_userlessonprogress', raise_exception=True)
def get_lesson_progress(request, lesson_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    try:
        lesson_progress = UserLessonProgress.objects.get(user_progress=user_progress, lesson=lesson)
        return lesson_progress.progress
    except UserLessonProgress.DoesNotExist:
        return 0


# @login_required
# @permission_required('progress.view_userlessonprogress', raise_exception=True)
def is_lesson_completed(request, lesson_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    try:
        lesson_progress = UserLessonProgress.objects.get(user_progress=user_progress, lesson=lesson)
        return lesson_progress.completed
    except UserLessonProgress.DoesNotExist:
        return False


# @login_required
# @permission_required('progress.view_userlessonprogress', raise_exception=True)
def is_lesson_started(request, lesson_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    try:
        lesson_progress = UserLessonProgress.objects.get(user_progress=user_progress, lesson=lesson)
        return lesson_progress.progress > 0
    except UserLessonProgress.DoesNotExist:
        return False


# @login_required
# @permission_required('progress.change_userlessonprogress', raise_exception=True)
def mark_lesson_as_completed(request, lesson_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    lesson_progress, created = UserLessonProgress.objects.get_or_create(user_progress=user_progress, lesson=lesson)
    lesson_progress.progress = 100
    lesson_progress.completed = True
    lesson_progress.save()

    course = lesson.course
    if check_course_completed(request, course.id):
        mark_course_as_completed(request, course.id)


# @login_required
# @permission_required('progress.view_userlessonprogress', raise_exception=True)
def check_lesson_completed(request, lesson_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    max_total_points = get_lesson_max_total_points(request, lesson_id)

    user_total_points = 0
    lesson_chapters = lesson.lessonchapter_set.all()
    for chapter in lesson_chapters:
        user_chapter_progresses = UserLessonChapterProgress.objects.filter(user_progress=user_progress, chapter=chapter)
        for user_chapter_progress in user_chapter_progresses:
            if user_chapter_progress.completed:
                chapter = user_chapter_progress.chapter
                points_for_chapter = get_lesson_chapter_max_total_points(request, chapter.id)
                user_total_points += points_for_chapter

    if user_total_points == max_total_points:
        return True
    else:
        return False
