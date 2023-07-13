from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission

# Register your models here.
from .models import UserProfile
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType

admin.site.register(UserProfile)

# Permission settings
# user_group, created = Group.objects.get_or_create(name="User")
# admin_group, created = Group.objects.get_or_create(name="Admin")
#
# models_list = [UserProfile,
#                Session,
#                User,
#                Group
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