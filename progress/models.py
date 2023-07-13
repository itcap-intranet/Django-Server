from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Lesson, LessonChapter, Assignment, Quiz
import datetime
from django.utils.translation import gettext_lazy as _



class UserProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_courses_num = models.IntegerField(default=0)
    completed_lessons_num = models.IntegerField(default=0)

class UserCourseProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default= 0)
    completion_date = models.DateField(default=datetime.date.today)
    completed = models.BooleanField(default=False)


class UserLessonProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    progress = models.IntegerField(default = 0)
    completion_date = models.DateField(default=datetime.date.today)
    completed = models.BooleanField(default=False)

class UserLessonChapterProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE)
    chapter = models.ForeignKey(LessonChapter, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completion_date = models.DateField(default=datetime.date.today)
    completed = models.BooleanField(default=False)


class UserAssignmentSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress_id = models.ForeignKey(UserProgress, on_delete=models.CASCADE, null=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    submission_file = models.FileField(null=True, blank=True, upload_to='static/assignments/')
    passed = models.BooleanField(default=False)
    total_points = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=datetime.datetime.now)


class UserQuizSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress_id = models.ForeignKey(UserProgress, on_delete=models.CASCADE, null=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    passed = models.BooleanField(default=False)
    total_points = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=datetime.datetime.now)

class UserActivityLedgerRecord(models.Model):
    id = models.AutoField(primary_key=True)
    user_progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    chapter = models.ForeignKey(LessonChapter, on_delete=models.CASCADE, null=True)
