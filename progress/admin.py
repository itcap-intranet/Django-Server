from django.contrib import admin

from .models import UserProgress, UserCourseProgress, UserLessonProgress, UserLessonChapterProgress, UserAssignmentSubmission, UserQuizSubmission, UserActivityLedgerRecord
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

# Register your models here.
admin.site.register(UserProgress)
admin.site.register(UserCourseProgress)
admin.site.register(UserLessonProgress)
admin.site.register(UserLessonChapterProgress)
admin.site.register(UserAssignmentSubmission)
admin.site.register(UserQuizSubmission)
admin.site.register(UserActivityLedgerRecord)



# Permission settings
# user_group, created = Group.objects.get_or_create(name="User")
# admin_group, created = Group.objects.get_or_create(name="Admin")
#
# models_list = [UserProgress,
#                UserLessonChapterProgress,
#                UserLessonProgress,
#                UserCourseProgress,
#                UserQuizSubmission,
#                UserAssignmentSubmission,
#                UserActivityLedgerRecord
#                ]
#
# for model in models_list:
#     content_type = ContentType.objects.get_for_model(model)
#     view_permission = Permission.objects.get(content_type=content_type, codename='view_%s' % model.__name__.lower())
#     add_permission = Permission.objects.get(content_type=content_type, codename='add_%s' % model.__name__.lower())
#     change_permission = Permission.objects.get(content_type=content_type, codename='change_%s' % model.__name__.lower())
#     delete_permission = Permission.objects.get(content_type=content_type, codename='delete_%s' % model.__name__.lower())
#
#     # Admin permissions
#     admin_group.permissions.add(view_permission)
#     admin_group.permissions.add(add_permission)
#     admin_group.permissions.add(change_permission)
#     admin_group.permissions.add(delete_permission)
#
#     # User permissions
#     user_group.permissions.add(view_permission)
#     user_group.permissions.add(add_permission)
#     user_group.permissions.add(change_permission)
#     user_group.permissions.add(delete_permission)