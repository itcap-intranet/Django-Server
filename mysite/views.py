from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import MyUserCreationForm
from . import api
from progress import views as progress_views
from courses.crud import course_crud, author_crud, lesson_crud, lesson_chapter_crud, video_crud, assignment_crud, quiz_crud, quiz_question_crud
from django.contrib.auth.models import Group
from courses.forms import AuthorForm, CourseForm, LessonForm, LessonChapterForm, VideoForm, AssignmentForm, QuizForm, QuizQuestionForm


from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
# Views
# @login_required
def home(request):
    # response = api.get_courses(request)
    context = {
        'top_learners': progress_views.get_top_learners_this_week(request),
        'course_activity_list': progress_views.get_course_activity_list(request),
        'active_courses': progress_views.get_active_courses(request),
    }

    return render(request, "index.html", context)

# @login_required
# @permission_required('courses.change_author', raise_exception=True)
def settings_authors(request):
    form = AuthorForm()
    context = {
        'authors': author_crud.get_authors(request),
        'form': form,
    }
    return render(request, "settings/sections/author_settings.html", context)

# @login_required
# @permission_required('courses.change_course', raise_exception=True)
def settings_courses(request):
    form = CourseForm()
    context = {
        'courses': course_crud.get_courses(request),
        'authors': author_crud.get_authors(request),
        'form': form,
    }
    return render(request, "settings/sections/course_settings.html", context)

# @login_required
# @permission_required('courses.change_lesson', raise_exception=True)
def settings_lessons(request):
    form = LessonForm()
    context = {
        'lessons': lesson_crud.get_lessons(request),
        'courses': course_crud.get_courses(request),
        'form': form,
    }
    return render(request, "settings/sections/lesson_settings.html", context)

# @login_required
# @permission_required('courses.change_lessonchapter', raise_exception=True)
def settings_lesson_chapters(request):
    form = LessonChapterForm()
    context = {
        'lesson_chapters': lesson_chapter_crud.get_lesson_chapters(request),
        'lessons': lesson_crud.get_lessons(request),
        'form': form,
    }
    return render(request, "settings/sections/lesson_chapter_settings.html", context)

# @login_required
# @permission_required('courses.change_lessonvideo', raise_exception=True)
def settings_videos(request):
    form = VideoForm()
    context = {
        'videos': video_crud.get_videos(request),
        'video_chapters': lesson_chapter_crud.get_lesson_chapters(request).filter(type='Video'),
        'form': form,

    }
    return render(request, "settings/sections/upload_video_settings.html", context)


# @login_required
# @permission_required('courses.change_quiz', raise_exception=True)
def settings_quizzes(request):
    form = QuizForm()
    form2 = QuizQuestionForm()

    context = {
        'quizzes': quiz_crud.get_quizzes(request),
        'quiz_chapters': lesson_chapter_crud.get_lesson_chapters(request).filter(type='Quiz'),
        'quiz_questions': quiz_question_crud.get_quiz_questions(request),
        'form': form,
        'form2': form2,
    }
    return render(request, "settings/sections/quiz_settings.html", context)

# @login_required
# @permission_required('courses.change_assignment', raise_exception=True)
def settings_assignments(request):
    form = AssignmentForm()
    context = {
        'assignments': assignment_crud.get_assignments(request),
        'assignment_chapters': lesson_chapter_crud.get_lesson_chapters(request).filter(type='Assignment'),
        'form': form,
    }
    return render(request, "settings/sections/assignment_settings.html", context)

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('username')

            user = authenticate(username=username, password=password)
            login(request, user)

            user.first_name = firstname
            user.last_name = lastname
            user.email = email

            # add user to the user group and give permissions
            user_group = Group.objects.get(name="User")
            user.groups.add(user_group)
            user.save()

            # create and save user progress
            progress_views.user_progress_crud.init_progress(request, user)

            return redirect('/home/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# @login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        print(request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # dont logout the user.
            # messages.success(request, "Password changed.")
            print("Password changed.")
            return redirect("/change-password")
        else:
            print("ERROR. Password not changed.")
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)

    data = {
        'form': form
    }
    return render(request, 'profile/change_password.html', data)




def server_error(request, exception=None):
    return render(request, 'registration/error500.html')

def permission_denied(request, exception=None):
    return redirect('/home/')

def page_not_found(request, exception=None):
     return render(request, 'registration/error404.html')

def bad_request(request, exception=None):
    return redirect('/home/')