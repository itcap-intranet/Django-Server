"""
URL configuration for athena_frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views as course_views
from courses.crud.course_crud import course_create_view, course_edit_view, course_delete_view
from courses.crud.author_crud import author_create_view, author_edit_view,  author_delete_view
from courses.crud.lesson_crud import lesson_create_view, lesson_edit_view, lesson_delete_view
from courses.crud.lesson_chapter_crud import lesson_chapter_create_view, lesson_chapter_edit_view, lesson_chapter_delete_view
from courses.crud.video_crud import video_create_view, video_edit_view, video_delete_view
from courses.crud.assignment_crud import assignment_create_view, assignment_edit_view, assignment_delete_view
from courses.crud.quiz_crud import quiz_create_view, quiz_edit_view, quiz_delete_view
from courses.crud.quiz_question_crud import quiz_question_create_view, quiz_question_edit_view, quiz_question_delete_view, manage_answers_view
from courses.crud.quiz_answer_crud import quiz_answer_create_view, quiz_answer_delete_view
from django.contrib.auth.decorators import login_required

app_name = 'courses'

urlpatterns = [

    # path('', login_required(course_views.CourseListView.as_view()), name='courses'),
    # path('<int:pk>', login_required(course_views.CourseDetailView.as_view()), name='course-details'),
    path('lesson/<int:lesson_id>/chapter/<int:chapter_id>', course_views.get_chapter_content, name='lesson-chapter-details'),

    path('create_course/', course_create_view, name='course-create'),
    path('edit_course/<int:course_id>', course_edit_view, name='course-edit'),
    path('delete_course/<int:course_id>', course_delete_view, name='course-delete'),

    path('create_author/', author_create_view, name='author-create'),
    path('edit_author/<int:author_id>', author_edit_view, name='author-edit'),
    path('delete_author/<int:author_id>', author_delete_view, name='author-delete'),

    path('create_lesson/', lesson_create_view, name='lesson-create'),
    path('edit_lesson/<int:lesson_id>', lesson_edit_view, name='lesson-edit'),
    path('delete_lesson/<int:lesson_id>', lesson_delete_view, name='lesson-delete'),

    path('create_lesson_chapter/', lesson_chapter_create_view, name='lesson-chapter-create'),
    path('edit_lesson_chapter/<int:lesson_chapter_id>', lesson_chapter_edit_view, name='lesson-chapter-edit'),
    path('delete_lesson_chapter/<int:lesson_chapter_id>', lesson_chapter_delete_view, name='lesson-chapter-delete'),

    path('create_video/', video_create_view, name='video-create'),
    path('edit_video/<int:video_id>', video_edit_view, name='video-edit'),
    path('delete_video/<int:video_id>', video_delete_view, name='video-delete'),

    path('create_quiz/', quiz_create_view, name='quiz-create'),
    path('edit_quiz/<int:quiz_id>', quiz_edit_view, name='quiz-edit'),
    path('delete_quiz/<int:quiz_id>', quiz_delete_view, name='quiz-delete'),

    path('create_quiz_question/', quiz_question_create_view, name='quiz-question-create'),
    path('edit_quiz_question/<int:quiz_question_id>', quiz_question_edit_view, name='quiz-question-edit'),
    path('manage_answers/<int:quiz_question_id>', manage_answers_view, name='manage-answers'),
    path('delete_quiz_question/<int:quiz_question_id>', quiz_question_delete_view, name='quiz-question-delete'),

    path('create_quiz_answer/<int:quiz_question_id>', quiz_answer_create_view, name='quiz-answer-create'),
    path('delete_quiz_answer/<int:quiz_answer_id>', quiz_answer_delete_view, name='quiz-answer-delete'),

    path('create_assignment/', assignment_create_view, name='assignment-create'),
    path('edit_assignment/<int:assignment_id>', assignment_edit_view, name='assignment-edit'),
    path('delete_assignment/<int:assignment_id>', assignment_delete_view, name='assignment-delete'),

]
