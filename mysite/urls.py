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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from courses import views as course_views
from django.shortcuts import render
from django.template import RequestContext
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.conf import settings
from django.conf.urls.static import static
from .api import api

urlpatterns = [
    path("api/", api.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change_password'),

    # path('change-password/', auth_views.PasswordChangeView.as_view(template_name='profile/change_password.html', success_url='/'), name='change_password'),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',
                                                                 html_email_template_name='registration/password_reset_email.html'),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),


    path('settings/authors', views.settings_authors, name='settings-authors'),
    path('settings/courses', views.settings_courses, name='settings-courses'),
    path('settings/lessons', views.settings_lessons, name='settings-lessons'),
    path('settings/lesson_chapters', views.settings_lesson_chapters, name='settings-lesson-chapters'),
    path('settings/videos', views.settings_videos, name='settings-videos'),
    path('settings/quizzes', views.settings_quizzes, name='settings-quizzes'),
    path('settings/assignments', views.settings_assignments, name='settings-assignments'),

    # path('settings/<int:tabid>', views.settings, name='settings'),

    path('admin/', admin.site.urls),
    path('progress/', include('progress.urls')),
    path('course/', include('courses.urls')),
    path('profile/', include('user_profile.urls')),
]

handler400 = 'mysite.views.bad_request'
handler403 = 'mysite.views.permission_denied'
handler404 = 'mysite.views.page_not_found'
handler500 = 'mysite.views.server_error'

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
