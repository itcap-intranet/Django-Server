from django import forms
from .models import Course, Author, Lesson, LessonChapter, LessonVideo, Assignment, Quiz, QuizQuestion, QuizAnswer
from django.forms import ModelChoiceField
from django.forms.fields import Field
setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput ))


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['author'].label_from_instance = self.author_label_from_instance

    @staticmethod
    def author_label_from_instance(obj):
        return obj.first_name + " " + obj.last_name

    class Meta:
        model = Course
        exclude = ["pub_date"]

class AuthorForm(forms.ModelForm):

    profile_pic_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'dropify', 'data-height': '200'}))
    class Meta:
        model = Author
        fields = "__all__"

class LessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['course'].label_from_instance = self.course_label_from_instance

    @staticmethod
    def course_label_from_instance(obj):
        return obj.name

    class Meta:
        model = Lesson
        fields = "__all__"

class LessonChapterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LessonChapterForm, self).__init__(*args, **kwargs)
        self.fields['lesson'].label_from_instance = self.lesson_label_from_instance

    @staticmethod
    def lesson_label_from_instance(obj):
        return obj.name + " - " + obj.course.name

    class Meta:
        model = LessonChapter
        fields = "__all__"

class VideoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['chapter'].label_from_instance = self.chapter_label_from_instance
        self.fields['chapter'].queryset = LessonChapter.objects.filter(type='Video')

    @staticmethod
    def chapter_label_from_instance(obj):
        return obj.name + " - " + obj.lesson.name

    class Meta:
        model = LessonVideo
        exclude = ["url","duration"]

class AssignmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['chapter'].label_from_instance = self.chapter_label_from_instance
        self.fields['chapter'].queryset = LessonChapter.objects.filter(type='Assignment')

    @staticmethod
    def chapter_label_from_instance(obj):
        return obj.name + " - " + obj.lesson.name


    class Meta:
        model = Assignment
        fields = "__all__"

class QuizForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['chapter'].label_from_instance = self.chapter_label_from_instance
        self.fields['chapter'].queryset = LessonChapter.objects.filter(type='Quiz')

    @staticmethod
    def chapter_label_from_instance(obj):
        return obj.name + " - " + obj.lesson.name

    class Meta:
        model = Quiz
        fields = "__all__"

class QuizQuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuizQuestionForm, self).__init__(*args, **kwargs)
        self.fields['quiz'].label_from_instance = self.quiz_label_from_instance

    @staticmethod
    def quiz_label_from_instance(obj):
        return obj.chapter.name + " in " + obj.chapter.lesson.name

    class Meta:
        model = QuizQuestion
        fields = "__all__"

class QuizAnswerForm(forms.ModelForm):

    class Meta:
        model = QuizAnswer
        fields = "__all__"
        widgets = {'question': forms.HiddenInput(), 'is_correct': forms.HiddenInput()}

        def __init__(self, *args, **kwargs):
            super(QuizAnswerForm, self).__init__(*args, **kwargs)

