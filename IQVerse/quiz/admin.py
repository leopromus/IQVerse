from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Teacher, Student, Course, Question, Marks, TeacherApplication


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Marks)

# Function to Create Roles and Assign Permissions
def create_roles_and_permissions():
    # Clear existing groups (optional, use carefully in production)
    Group.objects.all().delete()

    # Admin Group
    admin_group, created = Group.objects.get_or_create(name='Admin')

    # Teacher Group
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    teacher_permissions = Permission.objects.filter(
        content_type__model__in=['course', 'question']
    )
    teacher_group.permissions.set(teacher_permissions)

    # Student Group
    student_group, created = Group.objects.get_or_create(name='Student')
    student_permissions = Permission.objects.filter(
        content_type__model__in=['marks']
    )
    student_group.permissions.set(student_permissions)


# Call the function to create roles and assign permissions
create_roles_and_permissions()

admin.site.register(TeacherApplication)
