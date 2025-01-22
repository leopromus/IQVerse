from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage_teachers/', views.manage_teachers, name='manage_teachers'),
    path('admin/approve_teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),

    path('admin/manage_students/', views.manage_students, name='manage_students'),
    path('admin/edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('admin/delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('admin/settings/', views.settings, name='settings'),

    path('admin/manage_courses/', views.manage_courses, name='manage_courses'),
    path('admin/add_course/', views.add_course, name='add_course'),
    path('admin/delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    # Teacher
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add_course/', views.add_course, name='add_course'),
    path('admin/edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('admin/delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),


    #courses

    path('add_course/', views.add_course, name='add_course'),
    path('view_courses/', views.view_courses, name='view_courses'),
    path('update_course/<int:course_id>/', views.update_course, name='update_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    # Student
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    #path('dashboard/', views.student_dashboard_view, name='student-dashboard'),

    # questions

    #path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    #path('add_question/', views.add_question, name='add_question'),
    #path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),

    #path('manage_questions/', views.manage_questions, name='manage_questions'),
    path('add_question/', views.add_question, name='add_question'),
    # path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    # path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),

    path('exams/', views.manage_exams, name='manage_exams'),
    path('exams/<int:exam_id>/questions/', views.manage_questions, name='manage_questions'),
    path('exams/<int:exam_id>/add_question/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    # ... other URL patterns
    path('take_exam/<int:course_id>/', views.take_exam, name='take_exam'),
    path('view_results/', views.view_result_view, name='view_results'),  # URL for viewing results

    path('quiz/view_results/<int:attempt_id>/', views.view_results, name='view_results'),

    path('exams/manage/', views.manage_exams, name='manage_exams'),  # List all exams
    path('exam/create/', views.add_exam, name='add_exam'),  # Create a new exam
    path('exam/new/<int:exam_id>/', views.view_exam, name='view_exam'),  # View a specific exam
    path('exam/<int:exam_id>/edit/', views.edit_exam, name='edit_exam'),  # Edit a specific exam
    path('exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),  # Delete a specific exam

    # URL for submitting the exam
    path('submit_exam/<int:attempt_id>/', views.submit_exam, name='submit_exam'),

    path('not-enrolled/', views.not_enrolled_error, name='not_enrolled_error'),
    path('quiz/resume_exam/<int:attempt_id>/', views.resume_exam, name='resume_exam'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('exam/results/<int:attempt_id>/', views.exam_results, name='exam_results'),
    path('error/', views.error_page, name='error_page'),

    # Student exam related views
    path('exam/', views.student_exam_view, name='student-exam'),
    path('exam/<int:pk>/', views.take_exam_view, name='take-exam'),
    path('exam/start/<int:quiz_id>/', views.start_exam_view, name='start-exam'),

    # Result related views
    path('exam/calculate/', views.calculate_marks_view, name='calculate-marks'),
    path('results/', views.view_result_view, name='view-result'),
    path('results/<int:quiz_id>/', views.check_marks_view, name='check-marks'),
    path('marks/', views.student_marks_view, name='student-marks'),
    path('assign_exam/', views.assign_exam, name='assign_exam'),
    path('quiz-transcript/', views.quiz_transcript_view, name='quiz_transcript'),





    path('questions/', views.manage_questions, name='manage_questions'),
    path('questions/add/', views.add_question, name='add_question'),
    path('questions/update/<int:question_id>/', views.update_question, name='update_question'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),

    path('quizzes/', views.manage_quizzes, name='manage_quizzes'),
    path('quizzes/add/', views.add_quiz, name='add_quiz'),
    path('quizzes/update/<int:quiz_id>/', views.update_quiz, name='update_quiz'),
    path('quizzes/delete/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),

    path('reset_all_quizzes/', views.reset_all_quizzes, name='reset_all_quizzes'),
    path('reset_quiz/<int:quiz_id>/', views.reset_quiz, name='reset_quiz'),

]
