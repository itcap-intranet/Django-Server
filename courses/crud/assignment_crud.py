from courses.models import Assignment, LessonChapter
from courses.forms import AssignmentForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required


# @login_required
# @permission_required('courses.add_assignment', raise_exception=True)
def assignment_create_view(request):
    print('create assignment view')
    if request.method == 'POST':
        form = AssignmentForm(request.POST or None)

        if form.is_valid():
            print(form.cleaned_data)
            assignment = form.save()
            form = AssignmentForm()
        else:
            print('form is not valid')
            print(form.errors)

    else:
        form = AssignmentForm()

    data = {
        'form': form,
        'assignments': get_assignments(request),
    }

    return render(request, "settings/sections/assignment_settings.html", data)


# @login_required
# @permission_required('courses.view_assignment', raise_exception=True)
def get_assignments(request):
    assignments = Assignment.objects.all()
    return assignments


# @login_required
# @permission_required('courses.change_assignment', raise_exception=True)
def assignment_edit_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment_chapters = LessonChapter.objects.filter(type='Assignment')

    print('edit assignment view')
    form = AssignmentForm(request.POST or None, instance=assignment)

    if form.is_valid():
        assignment = form.save()
        return HttpResponseRedirect('/settings/assignments', {'form': form})
    else:
        print('form is not valid')
        print(form.errors)
        error = form.errors

    context = {
        'assignment': assignment,
        'assignment_chapters': assignment_chapters,
    }
    return render(request, "settings/sections/forms/edit_assignment.html", context)


# @login_required
# @permission_required('courses.delete_assignment', raise_exception=True)
def assignment_delete_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    return HttpResponseRedirect('/settings/assignments')
