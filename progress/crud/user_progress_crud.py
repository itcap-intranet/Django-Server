from progress.models import UserProgress, UserCourseProgress, UserLessonProgress, UserLessonChapterProgress
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from progress.crud.user_activity_crud import get_daily_activity_points, get_weekly_activity_points, \
    get_monthly_activity_points, get_total_activity_points
from courses.crud.course_crud import get_courses


# @login_required
# @permission_required('progress.add_userprogress', raise_exception=True)
def init_progress(request, user):
    print("init_progress")
    print(user)
    user_progress, created = UserProgress.objects.get_or_create(user_id=user)
    user_progress.save()
    return user_progress


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_user_progress_by_user(request, user):
    try:
        user_progress = UserProgress.objects.get(user_id=user)
    except UserProgress.DoesNotExist:
        user_progress = init_progress(request, user)
    return user_progress

# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_user_results_for_leaderboard(request):
    user_progresses = UserProgress.objects.all()

    for user_progress in user_progresses:

        user_progress.total_points = get_total_activity_points(request, user_progress.user_id)
        user_progress.weekly_points = get_weekly_activity_points(request, user_progress.user_id)
        user_progress.monthly_points = get_monthly_activity_points(request, user_progress.user_id)
        user_progress.daily_points = get_daily_activity_points(request, user_progress.user_id)
        user_progress.first_name = user_progress.user_id.first_name
        user_progress.last_name = user_progress.user_id.last_name

    return user_progresses


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_top_learners_this_week(request):
    user_progresses = UserProgress.objects.all()
    for user_progress in user_progresses:
        user_progress.weekly_points = get_weekly_activity_points(request, user_progress.user_id)

    user_progresses = sorted(user_progresses, key=lambda x: x.weekly_points, reverse=True)
    # user_results = UserProgress.objects.all().order_by('-weekly_points')[:5]
    return user_progresses[:5]


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_daily_points(request, user):
    daily_points = get_daily_activity_points(request, user)
    return daily_points


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_weekly_points(request, user):
    weekly_points = get_weekly_activity_points(request, user)
    return weekly_points


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_monthly_points(request, user):
    monthly_points = get_monthly_activity_points(request, user)
    return monthly_points


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_total_points(request, user):
    total_points = get_total_activity_points(request, user)
    return total_points


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_completed_lessons_num(request):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    user_lesson_progresses = UserLessonProgress.objects.filter(user_progress=user_progress)
    if user_lesson_progresses is None:
        return 0
    else:
        count = user_lesson_progresses.filter(completed=True).count()
        return count


# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_completed_courses_num(request):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    user_course_progresses = UserCourseProgress.objects.filter(user_progress=user_progress)
    if user_course_progresses is None:
        return 0
    else:
        count = user_course_progresses.filter(completed=True).count()
        return count

# @login_required
# @permission_required('progress.view_userprogress', raise_exception=True)
def get_active_courses(request):
    user_progress = get_object_or_404(UserProgress, user_id=request.user.id)
    user_course_progresses = UserCourseProgress.objects.filter(user_progress=user_progress)

    active_courses = {}

    for user_course_progress in user_course_progresses:
        if user_course_progress.completed == False and user_course_progress.progress > 0:
            active_courses[user_course_progress.course.id] = user_course_progress.course.name

    return active_courses