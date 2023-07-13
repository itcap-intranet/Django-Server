from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Course, Lesson, LessonChapter, LessonVideo, Quiz, QuizQuestion, QuizAnswer, Assignment, Author

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonChapter)
admin.site.register(LessonVideo)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(Assignment)
admin.site.register(Author)

# Permission settings
# user_group, created = Group.objects.get_or_create(name="User")
# admin_group, created = Group.objects.get_or_create(name="Admin")
#
# models_list = [Course,
#                Lesson,
#                LessonChapter,
#                LessonVideo,
#                Quiz,
#                QuizQuestion,
#                QuizAnswer,
#                Assignment,
#                Author
#                ]
#
# for model in models_list:
#     content_type = ContentType.objects.get_for_model(model)
#     view_permission = Permission.objects.get(content_type=content_type, codename='view_%s' % model.__name__.lower())
#     add_permission = Permission.objects.get(content_type=content_type, codename='add_%s' % model.__name__.lower())
#     change_permission = Permission.objects.get(content_type=content_type, codename='change_%s' % model.__name__.lower())
#     delete_permission = Permission.objects.get(content_type=content_type, codename='delete_%s' % model.__name__.lower())
#     print(view_permission, add_permission, change_permission, delete_permission)
#
#     # Admin permissions
#     admin_group.permissions.add(view_permission)
#     admin_group.permissions.add(add_permission)
#     admin_group.permissions.add(change_permission)
#     admin_group.permissions.add(delete_permission)
#
#     # User permissions
#     user_group.permissions.add(view_permission)



