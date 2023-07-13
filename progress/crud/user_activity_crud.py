from progress.models import UserProgress, UserLessonProgress, UserLessonChapterProgress, UserActivityLedgerRecord
from courses.models import Lesson, LessonChapter
from courses.crud.lesson_crud import get_lesson_max_total_points
from progress.crud.course_progress_crud import check_course_completed, mark_course_as_completed
from courses.crud.lesson_chapter_crud import get_lesson_chapter_max_total_points
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
import datetime

# @login_required
# @permission_required('progress.add_useractivityledgerrecord', raise_exception=True)
def record_activity(request, chapter_id, points):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    chapter = get_object_or_404(LessonChapter, id=chapter_id)

    activity_record, created = UserActivityLedgerRecord.objects.get_or_create(user_progress=user_progress,
                                                                              chapter=chapter,
                                                                              points=points)

# @login_required
# @permission_required('progress.view_useractivityledgerrecord', raise_exception=True)
def get_daily_activity_points(request, user):
    user_progress = get_object_or_404(UserProgress, user_id=user.id)

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    activity_records = UserActivityLedgerRecord.objects.filter(user_progress=user_progress, datetime__range=(today_min, today_max))
    if activity_records.count() == 0:
        return 0

    total_points = 0

    for record in activity_records:
        total_points += record.points

    return total_points


# @login_required
# @permission_required('progress.view_useractivityledgerrecord', raise_exception=True)
def get_weekly_activity_points(request, user):
    user_progress = get_object_or_404(UserProgress, user_id=user.id)

    td_1w = datetime.timedelta(weeks=1)

    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_min = today_max - td_1w

    activity_records = UserActivityLedgerRecord.objects.filter(user_progress=user_progress, datetime__range=(today_min, today_max))
    total_points = 0

    for record in activity_records:
        total_points += record.points

    return total_points


# @login_required
# @permission_required('progress.view_useractivityledgerrecord', raise_exception=True)
def get_monthly_activity_points(request, user):
    user_progress = get_object_or_404(UserProgress, user_id=user.id)

    td_1m = datetime.timedelta(days=30)

    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_min = today_max - td_1m

    activity_records = UserActivityLedgerRecord.objects.filter(user_progress=user_progress, datetime__range=(today_min, today_max))
    total_points = 0

    for record in activity_records:
        total_points += record.points

    return total_points


# @login_required
# @permission_required('progress.view_useractivityledgerrecord', raise_exception=True)
def get_total_activity_points(request, user):
    user_progress = get_object_or_404(UserProgress, user_id=user.id)

    activity_records = UserActivityLedgerRecord.objects.filter(user_progress=user_progress)
    total_points = 0

    for record in activity_records:
        total_points += record.points

    return total_points


# @login_required
# @permission_required('progress.view_useractivityledgerrecord', raise_exception=True)
def get_course_activity_list(request):
    user = request.user
    user_progress = get_object_or_404(UserProgress, user_id=user.id)

    activity_records = UserActivityLedgerRecord.objects.filter(user_progress=user_progress).order_by('-datetime')

    return activity_records