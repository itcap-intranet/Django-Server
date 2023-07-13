from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic

import mysite.api
from .models import Course, Lesson, LessonChapter, Quiz, QuizQuestion, QuizAnswer, Author, LessonVideo, Assignment
from django.http import JsonResponse
from progress import views as progress_views
from .forms import CourseForm, AuthorForm
from django.http import HttpResponseRedirect


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        context['courses'] = Course.objects.all()
        for course in context['courses']:
            setattr(course, 'course_stats', progress_views.get_course_stats(self.request, course.id))
        return context


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        context['course'] = self.object
        context['course_lessons'] = Lesson.objects.filter(course_id=self.object.id)
        for lesson in context['course_lessons']:
            setattr(lesson, 'lesson_stats', progress_views.get_lesson_stats(self.request, lesson.id))
            setattr(lesson, 'videos_num', get_lesson_items_num(self.request, lesson.id, 'Video'))
            setattr(lesson, 'quizzes_num', get_lesson_items_num(self.request, lesson.id, 'Quiz'))
            setattr(lesson, 'assignments_num', get_lesson_items_num(self.request, lesson.id, 'Assignment'))
        return context


class LessonDetailView(generic.DetailView):
    model = Lesson
    template_name = 'courses/lesson_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LessonDetailView, self).get_context_data(*args, **kwargs)
        context['lesson'] = self.object
        context['lesson_chapters'] = LessonChapter.objects.filter(lesson_id=self.object.id)
        for chapter in context['lesson_chapters']:
            setattr(chapter, 'chapter_stats', progress_views.get_chapter_stats(self.request, chapter.id))
        return context

# @login_required
def get_lesson_items_num(request, lesson_id, type):
    lesson_chapters = LessonChapter.objects.filter(lesson_id=lesson_id)
    num = 0
    for lesson_chapter in lesson_chapters:
        if lesson_chapter.type == type:
            num += 1
    return num

def get_chapter_content(request, lesson_id, chapter_id):
    print("TEST")
    print(lesson_id)
    print(chapter_id)

    lesson = Lesson.objects.get(id=lesson_id)
    chapter = LessonChapter.objects.get(id=chapter_id)

    lesson_chapters = LessonChapter.objects.filter(lesson=lesson)
    try:
        video = LessonVideo.objects.get(chapter=chapter)
    except LessonVideo.DoesNotExist:
        video = None

    try:
        quiz = Quiz.objects.get(chapter=chapter)
    except Quiz.DoesNotExist:
        quiz = None

    try:
        assignment = Assignment.objects.get(chapter=chapter)
    except Assignment.DoesNotExist:
        assignment = None

    for chapter in lesson_chapters:
        setattr(chapter, 'chapter_stats', progress_views.get_chapter_stats(request, chapter.id))

    data = {
        'lesson': lesson,
        'chapter': chapter,
        'lesson_chapters': lesson_chapters,
        'video': video,
        'quiz': quiz,
        'assignment': assignment,

    }

    return render(request, 'courses/lesson_chapter.html', data)