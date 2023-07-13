from courses.models import LessonVideo, Lesson, Assignment
from progress.forms import AssignmentSubmissionForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from progress.models import UserAssignmentSubmission, UserProgress
from progress.crud.user_progress_crud import get_user_progress_by_user
from progress.crud.user_activity_crud import record_activity
from progress.crud.chapter_progress_crud import get_chapter_progress, mark_chapter_as_completed
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

# @login_required
# @permission_required('progress.add_userassignmentsubmission', raise_exception=True)
def submit_assignment_view(request):
    form = AssignmentSubmissionForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        print(form.cleaned_data)
        user = request.user
        assignment_id = form.cleaned_data.get('assignment_id').id
        assignment = get_object_or_404(Assignment, id=assignment_id)

        user_progress = get_user_progress_by_user(request, user)
        form.instance.user_progress_id = user_progress

        total_points = check_assignment_submission(request, assignment_id)
        max_total_points = get_assignment_max_total_points(request, assignment_id)

        if (total_points == max_total_points):
            form.instance.total_points = total_points
            form.instance.passed = True
            user_assignment_submission = form.save()

            chapter_progress = get_chapter_progress(request, assignment.chapter.id)
            if chapter_progress.completed == False:
                record_activity(request, assignment.chapter.id, total_points)
                mark_chapter_as_completed(request, assignment.chapter.id)

        lesson = assignment.chapter.lesson
        context = {
            'lesson': lesson,
        }

        form = AssignmentSubmissionForm()

    else:
        print('form is not valid')
        print(form.errors)

    return HttpResponseRedirect('/course/lesson/' + str(lesson.id)+"/chapter/"+str(assignment.chapter.id), context)


# @login_required
# @permission_required('progress.view_userassignmentsubmission', raise_exception=True)
def get_assignment_max_total_points(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    total_points = assignment.points
    return total_points


# @login_required
# @permission_required('progress.view_userassignmentsubmission', raise_exception=True)
def check_assignment_submission(request, assignment_id):
    # later on, we will check the assignment submission
    # for now, we will just return max points

    assignment = get_object_or_404(Assignment, id=assignment_id)
    total_points = assignment.points

    return total_points


class ThanksForAssignmentView(generic.TemplateView):
    template_name = 'progress/thanks_for_assignment.html'


# @login_required
# @permission_required('progress.view_userassignmentsubmission', raise_exception=True)
def get_user_assignments(request):
    user = request.user
    user_progress = get_object_or_404(UserProgress, user_id=user.id)
    user_assignments = UserAssignmentSubmission.objects.filter(user_progress_id=user_progress)
    return user_assignments


# @login_required
# @permission_required('progress.delete_userassignmentsubmission', raise_exception=True)
def user_assignment_delete_view(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignmentSubmission, id=user_assignment_id)
    user_assignment.delete()
    return HttpResponseRedirect('/progress/my_progress/')
