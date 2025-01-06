from django.urls import path
from . import views

from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),  # Home page

    # Teacher Signup
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'), # Logout URL
    #path('dashboard-redirect/', views.redirect_to_dashboard, name='dashboard_redirect'),

    path('teacher_signup/', views.teacher_signup, name='teacher_signup'),

    path('student_signup/', views.student_signup, name='student_signup'),# Admin Views
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/teacher/approve/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('approve-application/<int:application_id>/', views.approve_teacher_application, name='approve_teacher_application'),
    path('teacher/application-status/', views.teacher_application_status, name='teacher_application_status'),

    path('teacher/pending/', views.pending_teachers, name='pending_teachers'),


    path('admin/teacher/manage/<int:teacher_id>/', views.manage_teacher, name='manage_teacher'),
    path('admin/teacher/manage/', views.manage_teacher, name='manage_teacher_create'),
    path('admin/student/manage/<int:student_id>/', views.manage_student, name='manage_student'),
    path('admin/student/manage/', views.manage_student, name='manage_student_create'),
    path('admin/course/manage/<int:course_id>/', views.manage_course, name='manage_course'),
    path('admin/course/manage/', views.manage_course, name='manage_course_create'),
    path('admin/question/manage/<int:question_id>/', views.manage_question, name='manage_question'),
    path('admin/question/manage/', views.manage_question, name='manage_question_create'),

    # Teacher Dashboard
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Student Dashboard
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    # URL for taking an exam
    path('quiz/take-exam/<int:course_id>/', views.take_exam, name='take_exam'),

    # URL for viewing marks
    path('marks/', views.view_marks, name='view_marks'),  # For students
    path('admin/marks/', views.view_marks, name='admin_view_marks'),  # Admin viewing all marks
    path('admin/marks/<int:student_id>/', views.view_marks, name='admin_view_specific_marks'),
    # Admin viewing specific student marks

    # URL for exam guidelines
    path('quiz/exam-guidelines/', views.exam_guidelines, name='exam_guidelines'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('teacher-apply/', views.teacher_apply, name='teacher_apply'),
    path('add-course/', views.add_course, name='add_course'),
    path('view-courses/', views.view_courses, name='view_courses'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),
    path('add-question/', views.add_question, name='add_question'),
    path('view-questions/', views.view_questions, name='view_questions'),
    path('delete-question/<int:id>/', views.delete_question, name='delete_question'),
    path('approve_teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('update_teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),

    # Student Management
    path('update_student/<int:student_id>/', views.update_student, name='update_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
]
