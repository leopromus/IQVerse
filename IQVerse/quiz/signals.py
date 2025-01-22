# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User, Group
# from django.core.exceptions import ObjectDoesNotExist
#
# # Signal to automatically assign a role to a new user
# @receiver(post_save, sender=User)
# def assign_role(sender, instance, created, **kwargs):
#     if created:
#         try:
#             # Default group assignment (you can change the logic here)
#             default_group = Group.objects.get(name='Student')  # Default role is Student
#             instance.groups.add(default_group)
#
#             # Optionally, you can assign permissions based on the group
#             if default_group.name == 'Admin':
#                 instance.user_permissions.add(*['add_user', 'change_user', 'delete_user'])  # Example permissions for Admin
#             elif default_group.name == 'Teacher':
#                 instance.user_permissions.add(*['view_course', 'add_course'])  # Example permissions for Teacher
#             # Further permissions can be added here based on roles
#
#         except ObjectDoesNotExist:
#             print("Group does not exist, please create the necessary groups first.")
