from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    bio = models.CharField(null=True, blank=True, max_length=2000)
    profile_pic_file = models.FileField(null=True, blank=True, upload_to='static/authors/')
    facebook_url = models.CharField(max_length=1000, null=True, blank=True, validators=[URLValidator()])
    instagram_url = models.CharField(max_length=1000, null=True, blank=True, validators=[URLValidator()])




class Course(models.Model):
    class Level(models.TextChoices):
        BASIC = "Basic", _("Basic")
        INTERMEDIATE = "Intermediate", _("Intermediate")
        ADVANCED = "Advanded", _("Advanced")

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    headline = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, null=True)
    pub_date = models.DateTimeField('date published', null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, default= None, null=True)
    level = models.CharField(choices = Level.choices, default=Level.BASIC, max_length=200)
    course_small_image = models.FileField(null=True, blank=True, upload_to='static/courses/')
    course_large_image = models.FileField(null=True, blank=True, upload_to='static/courses/')


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class LessonChapter(models.Model):
    class LessonChapterType(models.TextChoices):
        VIDEO = "Video", _("Video")
        QUIZ = "Quiz", _("Quiz")
        ASSIGNMENT = "Assignment", _("Assignment")

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(choices = LessonChapterType.choices, default=LessonChapterType.VIDEO, max_length=200)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class LessonVideo(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000, blank=True, null=True, validators=[URLValidator()])
    video_file = models.FileField(null=True, blank=True, upload_to='static/media/')
    duration = models.IntegerField(null=True, blank=True, default=0)
    points = models.IntegerField(null=True, default=100)
    chapter = models.ForeignKey(LessonChapter, on_delete=models.CASCADE)


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(LessonChapter, on_delete=models.CASCADE)

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    points = models.IntegerField(default=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class QuizAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=1000)
    is_correct = models.BooleanField()
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True)

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=1000)
    points = models.IntegerField()
    chapter = models.ForeignKey(LessonChapter, on_delete=models.CASCADE)
