from progress.models import UserProgress, UserLessonChapterProgress, LessonChapter
from progress.crud.lesson_progress_crud import check_lesson_completed, mark_lesson_as_completed
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

# @login_required
# @permission_required('progress.view_userlessonchapterprogress', raise_exception=True)
def get_chapter_progress_percentage(request, lesson_chapter_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)

    try:
        lesson_chapter_progress = UserLessonChapterProgress.objects.get(user_progress=user_progress, chapter=chapter)
        return lesson_chapter_progress.progress
    except UserLessonChapterProgress.DoesNotExist:
        return 0

# @login_required
# @permission_required('progress.view_userlessonchapterprogress', raise_exception=True)
def get_chapter_progress(request, lesson_chapter_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)

    try:
        lesson_chapter_progress = UserLessonChapterProgress.objects.get(user_progress=user_progress, chapter=chapter)
        return lesson_chapter_progress
    except UserLessonChapterProgress.DoesNotExist:
        chapter = UserLessonChapterProgress(user_progress=user_progress, chapter=chapter, progress=0, completed=False)
        chapter.save()
        return chapter

# @login_required
# @permission_required('progress.view_userlessonchapterprogress', raise_exception=True)
def is_chapter_completed(request, lesson_chapter_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)

    try:
        lesson_chapter_progress = UserLessonChapterProgress.objects.get(user_progress=user_progress, chapter=chapter)
        return lesson_chapter_progress.completed
    except UserLessonChapterProgress.DoesNotExist:
        return False

# @login_required
# @permission_required('progress.view_userlessonchapterprogress', raise_exception=True)
def is_chapter_started(request, lesson_chapter_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)

    try:
        lesson_chapter_progress = UserLessonChapterProgress.objects.get(user_progress=user_progress, chapter=chapter)
        return lesson_chapter_progress.progress > 0
    except UserLessonChapterProgress.DoesNotExist:
        return False

# @login_required
# @permission_required('progress.change_userlessonchapterprogress', raise_exception=True)
def mark_chapter_as_completed(request, lesson_chapter_id):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=lesson_chapter_id)

    lesson_chapter_progress, created = UserLessonChapterProgress.objects.get_or_create(user_progress=user_progress, chapter=chapter)
    lesson_chapter_progress.progress = 100
    lesson_chapter_progress.completed = True
    print('marking chapter as completed')
    lesson_chapter_progress.save()

    lesson = chapter.lesson
    if check_lesson_completed(request, lesson.id):
        mark_lesson_as_completed(request, lesson.id)
        print('marking lesson is completed')
