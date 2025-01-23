from datetime import timezone, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from . import forms
from .models import User, Teacher, Student, Course, Question, Marks, TeacherApplication, Settings, Quiz, \
    UserQuizAttempt, Choice, UserAnswer, Leaderboard, QuizAttemptHistory, Testimonial
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import TeacherApplicationForm, QuestionForm, CourseForm, UserForm, StudentForm, CustomAuthenticationForm, \
    SettingsForm, ExamForm

from django.shortcuts import render, get_object_or_404
from .models import UserQuizAttempt, Question, Choice, UserAnswer
from django.utils import timezone

from django.core.paginator import Paginator

from .utils import calculate_quiz_score
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
# views.py
from django.shortcuts import render, redirect
from .forms import AssignExamForm
from django.contrib import messages
from django.shortcuts import render
from django.http import Http404
from .models import Student, Marks, UserAnswer  # Make sure to import the correct models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.timezone import now
from .models import UserQuizAttempt, UserAnswer, QuizAttemptHistory, Leaderboard

from django.core.exceptions import ObjectDoesNotExist

# Helpers
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# def is_teacher(user):
#     return user.is_authenticated and user.role == 'teacher'

def is_teacher_or_admin(user):
    return user.role in ['teacher', 'admin']

def is_teacher_admin_or_student(user):
    return user.role in ['teacher', 'admin', 'student']


def is_student(user):
    return user.is_authenticated and user.role == 'student'


def home(request):
    testimonials = Testimonial.objects.all()
    context = {
    'testimonials': testimonials
    }
    if request.user.is_authenticated and request.user.role == 'admin':
        context['total_users'] = User.objects.count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        context['total_students'] = User.objects.filter(role='student').count()
        context['teacher_applications'] = TeacherApplication.objects.all()
    return render(request, 'home.html', context)



def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Save the User model instance
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Handle Student signup
            if user.role == 'student':
                Student.objects.create(
                    user=user,
                    grade=form.cleaned_data['grade'],
                    parent_contact=form.cleaned_data['parent_contact']
                )
                messages.success(request, 'Account created successfully. Welcome to the student dashboard!')
                login(request, user)  # Log the student in automatically
                return redirect('student_dashboard')

            # Handle Teacher signup
            elif user.role == 'teacher':
                Teacher.objects.create(
                    user=user,
                    subject=form.cleaned_data['subject'],
                    experience=form.cleaned_data['experience'],
                    qualification=form.cleaned_data['qualification'],
                    is_approved=False  # Pending approval by admin
                )
                messages.info(request, 'Your account has been created and is pending admin approval.')
                return redirect('login')  # Redirect to login page with info message

        else:
            messages.error(request, 'There were errors in your form. Please try again.')
    else:
        form = UserForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                try:
                    # Check if the user is a teacher and has a teacher profile
                    if user.role == 'teacher':
                        if not hasattr(user, 'teacher'):
                            # Redirect to signup if no teacher profile exists
                            messages.error(
                                request,
                                "You must have a valid teacher profile to log in. Please sign up as a teacher."
                            )
                            return redirect('signup')

                        # Check if the teacher's account is approved
                        if not user.teacher.is_approved:
                            messages.error(
                                request,
                                "Your teacher account is not yet approved by the admin. Please wait for approval."
                            )
                            return redirect('login')

                    # Log the user in
                    login(request, user)

                    # Redirect based on user role
                    if user.role == 'admin':
                        return redirect('admin_dashboard')
                    elif user.role == 'teacher':
                        return redirect('teacher_dashboard')
                    elif user.role == 'student':
                        return redirect('student_dashboard')

                except ObjectDoesNotExist:
                    # Handle cases where the related object (e.g., Teacher) does not exist
                    messages.error(
                        request,
                        "An error occurred while accessing your account. Please contact support."
                    )
                    return redirect('login')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Form is invalid. Please check your input.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')


# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')

    # Get all exams to pass them to the template
    exams = Quiz.objects.all()

    # Prepare context data
    context = {
        'total_students': User.objects.filter(role='student').count(),
        'total_teachers': User.objects.filter(role='teacher').count(),
        'total_stu': Student.objects.count(),
        'total_teach': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
        'total_questions': Question.objects.count(),
        'exams': exams,  # Add exams to context
    }

    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'admin/manage_teachers.html', {'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def approve_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.is_approved = True
    teacher.save()
    messages.success(request, 'Teacher approved successfully.')
    return redirect('manage_teachers')


# Teacher Views
@login_required
@user_passes_test(is_teacher_or_admin)
def teacher_dashboard(request):
    # Fetch quizzes created by the current teacher
    # Assuming the teacher field in Quiz is now properly set and non-nullable
    exams = Quiz.objects.filter(title=request.user.teacher)  # Filter quizzes by the current teacher

    # Fetch total questions related to the quizzes created by the teacher
    questions_count = Question.objects.filter(quiz__in=exams).count()

    # Fetch total students if applicable
    students_count = Student.objects.count() if hasattr(Student, 'id') else 0

    # Fetch total courses taught by the current teacher
    courses_count = Course.objects.filter(teacher=request.user.teacher).count()  # Filter courses by the teacher

    context = {
        'students': students_count,
        'courses': courses_count,
        'questions': questions_count,
        'exams': exams,
    }
    return render(request, 'teacher/dashboard.html', context)

@login_required
@user_passes_test(is_teacher_or_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)

            # Automatically set teacher for teachers
            if request.user.role == 'teacher':
                course.teacher = request.user.teacher

            course.save()
            messages.success(request, 'Course added successfully.')

            # Redirect based on user role
            return redirect('teacher_dashboard' if request.user.role == 'teacher' else 'admin_dashboard')
    else:
        # If the user is a teacher, restrict the teacher selection to themselves
        if request.user.role == 'teacher':
            form = CourseForm(initial={'teacher': request.user.teacher})
            form.fields['teacher'].widget = forms.HiddenInput()  # Hide the teacher field
        else:
            form = CourseForm()  # Admin can choose any teacher

    return render(request, 'teacher/add_course.html', {'form': form})


@login_required
@user_passes_test(is_teacher_admin_or_student)  # Allow teachers, admins, and students to access this view
def view_courses(request):
    if request.user.role == 'teacher':
        # Teachers only see their courses
        courses = Course.objects.filter(teacher=request.user.teacher)
        return render(request, 'teacher/view_courses.html', {'courses': courses})
    elif request.user.role == 'student':
        # Students see all available courses
        courses = Course.objects.all()
        return render(request, 'student/view_courses.html', {'courses': courses})
    else:
        # Admin sees all courses
        courses = Course.objects.all()
        return render(request, 'admin/view_courses.html', {'courses': courses})

@login_required
@user_passes_test(is_teacher_or_admin)
def update_course(request, course_id):
    # Get the course or 404 if not found
    course = get_object_or_404(Course, id=course_id)

    # Check if the teacher owns the course
    if request.user.role == 'teacher' and course.teacher != request.user.teacher:
        messages.error(request, 'You are not authorized to edit this course.')
        return redirect('view_courses')

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('view_courses')
    else:
        form = CourseForm(instance=course)

    return render(request, 'teacher/update_course.html', {'form': form, 'course': course})

@login_required
@user_passes_test(is_teacher_or_admin)
def delete_course(request, course_id):
    # Get the course or 404 if not found
    course = get_object_or_404(Course, id=course_id)

    # Check if the teacher owns the course
    if request.user.role == 'teacher' and course.teacher != request.user.teacher:
        messages.error(request, 'You are not authorized to delete this course.')
    else:
        course.delete()
        messages.success(request, 'Course deleted successfully.')

    return redirect('view_courses')

# crud for questions




# @login_required
# @user_passes_test(is_teacher_or_admin)
# def manage_exams(request):
#     exams = Quiz.objects.all()  # Fetch all exams from the database
#     return render(request, 'admin/manage_exams.html', {'exams': exams})


@login_required
@user_passes_test(is_teacher_or_admin)
def manage_exams(request):
    exams = Quiz.objects.all()  # Fetch all exams from the database
    return render(request, 'admin/manage_exams.html', {'exams': exams})

@login_required
@user_passes_test(is_teacher_or_admin)
def manage_questions(request, exam_id):
    exam = get_object_or_404(Quiz, id=exam_id)  # Fetch the exam by its ID
    questions = exam.questions.all()  # Fetch all questions for this exam

    if request.method == 'POST':
        # Handle adding new questions
        if 'add_question' in request.POST:
            form = QuestionForm(request.POST)
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.quiz = exam  # Associate the question with the exam
                new_question.save()
                return redirect('manage_questions', exam_id=exam.id)  # Redirect after saving
        # Handle deleting a question
        elif 'delete_question' in request.POST:
            question_id = request.POST.get('delete_question')
            question = get_object_or_404(Question, id=question_id)
            question.delete()
            return redirect('manage_questions', exam_id=exam.id)  # Redirect after deleting

    # Form for adding a new question
    form = QuestionForm()

    return render(request, 'admin/manage_questions.html', {
        'exam': exam,
        'questions': questions,
        'form': form
    })


@login_required
@user_passes_test(is_teacher_or_admin)
def add_question(request, exam_id):
    # Fetch the exam using exam_id
    exam = get_object_or_404(Quiz, id=exam_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = exam  # Link the question to the specific exam
            question.save()
            # Redirect to the manage_questions view with the exam_id
            return redirect('manage_questions', exam_id=exam.id)
    else:
        form = QuestionForm()

    # Render the form to add a new question, passing the exam context
    return render(request, 'admin/add_question.html', {'form': form, 'exam': exam})




@login_required
@user_passes_test(is_teacher_or_admin)
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_exams')
    else:
        form = ExamForm()
    return render(request, 'admin/add_exam.html', {'form': form})

@login_required
@user_passes_test(is_teacher_or_admin)
def view_exam(request, exam_id):
    exam = get_object_or_404(Quiz, id=exam_id)
    return render(request, 'admin/view_exam.html', {'exam': exam})

@login_required
@user_passes_test(is_teacher_or_admin)
def edit_exam(request, exam_id):
    exam = get_object_or_404(Quiz, id=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('manage_exams')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'admin/edit_exam.html', {'form': form, 'exam': exam})

@login_required
@user_passes_test(is_teacher_or_admin)
def delete_exam(request, exam_id):
    exam = get_object_or_404(Quiz, id=exam_id)
    if request.method == 'POST':
        exam.delete()
        return redirect('manage_exams')
    return render(request, 'admin/delete_exam.html', {'exam': exam})


# @login_required
# @user_passes_test(is_teacher_or_admin)  # Ensure that only teachers can manage questions
# def manage_questions(request):
#     if request.user.role == 'teacher':
#         # Filter questions based on the courses the teacher is associated with
#         questions = Question.objects.filter(course__teacher=request.user.teacher)
#     else:
#         # Admin can view all questions
#         questions = Question.objects.all()
#
#     return render(request, 'admin/manage_questions.html', {'questions': questions})


# @login_required
# @user_passes_test(is_teacher_or_admin)
# def add_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             # If the user is a teacher, associate the question with the courses they are teaching
#             if request.user.role == 'teacher':
#                 course = Course.objects.filter(teacher=request.user.teacher).first()
#                 question.course = course  # Set the course for the question
#             question.save()
#             messages.success(request, 'Question added successfully.')
#             return redirect('manage_questions')
#     else:
#         form = QuestionForm()
#     return render(request, 'admin/add_question.html', {'form': form})


@login_required
@user_passes_test(is_teacher_or_admin)
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # Ensure the teacher can only edit questions from their own courses
    if request.user.role == 'teacher' and question.course.teacher != request.user.teacher:
        messages.error(request, 'You are not authorized to edit this question.')
        return redirect('manage_questions')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully.')
            return redirect('manage_questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin/edit_question.html', {'form': form, 'question': question})


@login_required
@user_passes_test(is_teacher_or_admin)
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # Ensure the teacher can only delete questions from their own courses
    if request.user.role == 'teacher' and question.course.teacher != request.user.teacher:
        messages.error(request, 'You are not authorized to delete this question.')
        return redirect('manage_questions')

    question.delete()
    messages.success(request, 'Question deleted successfully.')
    return redirect('manage_questions')


# Assuming `is_student` is a function that checks if the user is a student
@login_required
@user_passes_test(is_student)  # Ensures only students can access this view
def student_dashboard(request):
    student = request.user.student
    courses = student.courses.all()  # Get the courses that the student is enrolled in
    quizzes = Quiz.objects.filter(course__in=courses)  # Get quizzes for the student's enrolled courses
    questions = Question.objects.filter(course__in=courses)  # Get all questions for enrolled courses

    context = {
        'courses_count': courses.count(),
        'quizzes_count': quizzes.count(),
        'questions_count': questions.count(),
        'courses': courses,
        'quizzes': quizzes,
    }

    return render(request, 'student_dashboard.html', context)


# views.py
@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    # If the quiz is attempted before, retrieve the attempt data
    attempt, created = UserQuizAttempt.objects.get_or_create(
        user=request.user,
        quiz=quiz,
        completed=False
    )

    if request.method == "POST":
        # Process the submitted answers and calculate the score
        score = 0
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            correct_option = question.correct_option

            # Check if the selected answer is correct
            is_correct = selected_option == correct_option
            if is_correct:
                score += question.marks

            # Save the user answer
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                choice=question.choice_set.get(id=selected_option),
                is_correct=is_correct
            )

        # Mark the attempt as completed and save the score
        attempt.score = score
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        return redirect('quiz_results', attempt_id=attempt.id)

    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt
    }

    return render(request, 'student/take_quiz.html', context)


# views.py

@login_required
def quiz_results(request, attempt_id):
    attempt = UserQuizAttempt.objects.get(id=attempt_id)
    user_answers = attempt.answers.all()  # Retrieve all user answers for this attempt

    context = {
        'attempt': attempt,
        'user_answers': user_answers,
    }

    return render(request, 'quiz_results.html', context)


@login_required
def manage_teachers(request):
    if request.user.role != 'admin':
        return redirect('home')

    # Fetching teachers (with related Teacher model details)
    teachers = Teacher.objects.all()

    # Fetching teacher applications (pending approval)
    teacher_applications = TeacherApplication.objects.filter(approved=False)

    # Passing the data to the template
    return render(request, 'teacher/manage_teachers.html', {
        'teachers': teachers,
        'teacher_applications': teacher_applications
    })

def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        # Handle the form submission to update teacher details
        # For example, updating teacher's subject and experience
        teacher.subject = request.POST['subject']
        teacher.experience = request.POST['experience']
        teacher.save()
        return redirect('manage_teachers')

    return render(request, 'teacher/edit_teacher.html', {'teacher': teacher})

def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        # Delete the teacher from the database
        teacher.delete()
        return redirect('manage_teachers')  # Redirect back to the teacher management page

    return render(request, 'teacher/confirm_delete_teacher.html', {'teacher': teacher})



# def manage_students(request):
#     if request.user.role != 'admin':
#         return redirect('home')
#     students = User.objects.filter(role='student')
#     return render(request, 'manage_students.html', {'students': students})
#

@login_required
def manage_students(request):
    if request.user.role != 'admin':
        return redirect('home')  # Redirect to home if user is not an admin

    # Get all students
    students = User.objects.filter(role='student')

    # Handle student creation
    if request.method == 'POST' and 'add_student' in request.POST:
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = form.cleaned_data['user']  # Associate the user
            student.save()
            messages.success(request, "Student added successfully!")
            return redirect('manage_students')  # Redirect to manage students after adding

    else:
        form = StudentForm()

    return render(request, 'admin/manage_students.html', {'students': students, 'form': form})



def edit_student(request, student_id):
    # Ensure that only admin users can edit students
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to edit student details.")

    # Fetch the student by student_id (not user_id)
    student = get_object_or_404(Student, id=student_id)

    # Process the form submission
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student {student.user.username}'s details updated successfully!")
            return redirect('manage_students')  # Redirect to manage students after editing
    else:
        form = StudentForm(instance=student)

    # Render the edit student form
    return render(request, 'admin/edit_student.html', {'form': form, 'student': student})

def delete_student(request, student_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to delete students.")

    student = get_object_or_404(Student, id=student_id)
    student.user.delete()  # Deleting the associated User model entry (which deletes the Student too)
    messages.success(request, f"Student {student.user.username} deleted successfully!")
    return redirect('manage_students')  # Redirect to manage students after deleting


def settings(request):
    # Check if the user is an admin
    if request.user.role != 'admin':
        return redirect('home')  # Redirect to home if user is not admin

    # Get existing settings or create new ones if not available
    settings = Settings.get_settings()

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()  # Save the form data to the Settings model
            messages.success(request, "Settings updated successfully!")
            return redirect('settings')  # Redirect to settings page after saving
    else:
        form = SettingsForm(instance=settings)  # Pre-populate form with existing settings

    return render(request, 'admin/settings.html', {'form': form})


@login_required
@user_passes_test(is_teacher_or_admin)
def manage_courses(request):
    # Allow access only if the user is a teacher or an admin
    if request.user.role not in ['teacher', 'admin']:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    # Fetch courses based on the user's role
    if request.user.role == 'admin':
        courses = Course.objects.all()  # Admin can manage all courses
        template = 'admin/manage_courses.html'
    elif request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user.teacher)  # Teachers can manage their courses
        template = 'teacher/manage_courses.html'

    return render(request, template, {'courses': courses})

def some_view(request):
    settings = Settings.get_settings()
    return render(request, 'some_template.html', {'settings': settings})


# In the User or Student model

#
# def is_student_in_course(self, course):
#     return Student.objects.filter(user=self, course=course).exists()
#


def not_enrolled_error(request):
    return render(request, 'student/not_enrolled_error.html')

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    try:
        student = request.user.student
        if not student.is_enrolled_in_course(course):
            student.enrolled_courses.add(course)  # Enroll the student
            messages.success(request, f"You have been enrolled in {course.name}.")
        else:
            messages.info(request, "You are already enrolled in this course.")
    except Student.DoesNotExist:
        messages.error(request, "You must be a student to enroll in courses.")
        return redirect('home')

    return redirect('student/course_detail.html', course_id=course_id)


@login_required
@user_passes_test(is_teacher_admin_or_student)
def resume_exam(request, attempt_id):
    """
    Allows a user to resume an incomplete quiz attempt, or reset a completed one to submit new answers.
    """
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)

    # Reset completed attempt for new submission
    if attempt.completed:
        attempt.score = 0  # Reset the score
        attempt.completed = False  # Mark as not completed
        attempt.completed_at = None  # Clear completed_at timestamp
        attempt.answers.all().delete()  # Clear previous answers
        attempt.save()

    quiz = attempt.quiz

    if request.method == 'POST':
        # Handle submission of remaining answers
        correct_answers = 0

        for question in quiz.questions_in_quiz.all():
            student_answer = request.POST.get(f"question_{question.id}")
            if student_answer:
                try:
                    selected_option = int(student_answer)
                    if selected_option in range(1, 5):  # Validate range
                        is_correct = str(selected_option) == question.correct_option

                        # Save new answer
                        UserAnswer.objects.create(
                            attempt=attempt,
                            question=question,
                            selected_option=selected_option,
                            is_correct=is_correct
                        )

                        if is_correct:
                            correct_answers += 1
                except ValueError:
                    messages.error(request, f"Invalid selection for question {question.id}. Please try again.")

        total_questions = quiz.questions_in_quiz.count()
        attempt.score = calculate_quiz_score(quiz, correct_answers, total_questions)
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        # Update leaderboard
        Leaderboard.objects.update_or_create(
            quiz=quiz,
            user=request.user,
            defaults={'score': attempt.score}
        )

        return redirect('view_results', attempt_id=attempt.id)

    # Handle GET requests to show unanswered questions
    answered_question_ids = attempt.answers.values_list('question_id', flat=True)
    unanswered_questions = quiz.questions_in_quiz.exclude(id__in=answered_question_ids)

    selected_answers = {
        answer.question.id: answer.selected_option
        for answer in attempt.answers.all()
    }

    return render(request, 'student/resume_exam.html', {
        'quiz': quiz,
        'attempt': attempt,
        'unanswered_questions': unanswered_questions,
        'selected_answers': selected_answers,
    })

@login_required
@user_passes_test(lambda user: hasattr(user, 'student'), login_url='login')
def take_exam(request, course_id):
    # Fetch the course object
    course = get_object_or_404(Course, id=course_id)

    # Ensure the user is a student
    if not hasattr(request.user, 'student'):
        return redirect('error_page')  # Redirect to an error page if the user is not a student

    student = request.user.student

    # Fetch the quizzes related to the course
    quizzes = Quiz.objects.filter(questions_in_quiz__course=course).distinct()

    # Check if the course has any quizzes associated
    if not quizzes.exists():
        return render(request, 'student/no_quizzes.html', {'course': course})

    # Assume the student starts the first quiz
    quiz = quizzes.first()

    # Check if the user has already attempted this quiz and not yet completed
    existing_attempt = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz, completed=False).first()
    if existing_attempt:
        # Redirect if an attempt is in progress
        return redirect('error_page')  # Redirect to an error page or allow resumption

    # Create a new quiz attempt
    attempt = UserQuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=0,
        started_at=timezone.now(),
        completed=False
    )

    # Handle the POST request for quiz submission
    if request.method == 'POST':
        total_score = 0  # Initialize total score
        max_score = 0   # Sum of all possible marks for the quiz

        # Process each question and validate answers based on correct_option
        for question in quiz.questions_in_quiz.all():
            student_answer = request.POST.get(f"question_{question.id}")
            if student_answer:
                # Check if the student's answer matches the correct option
                is_correct = student_answer == question.correct_option
                if is_correct:
                    total_score += question.marks  # Add marks if correct

                # Save the student's answer
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=student_answer,  # Save the selected option text
                    is_correct=is_correct
                )

            # Add to the max score regardless of the correctness
            max_score += question.marks

        # Calculate the score as a percentage
        score_percentage = (total_score / max_score) * 100 if max_score > 0 else 0

        # Update the attempt with the calculated score
        attempt.score = score_percentage
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        # Save the score to the leaderboard
        Leaderboard.objects.create(quiz=quiz, user=request.user, score=score_percentage)

        # Redirect to the result page with the score
        return render(request, 'student/view_results.html', {
            'score': score_percentage,
            'quiz': quiz,
            'total_score': total_score,
            'max_score': max_score
        })

    # If it's a GET request, paginate the quiz questions
    questions = quiz.questions_in_quiz.all()  # Ensure we are working with the full queryset
    paginator = Paginator(questions, 1)  # Show 1 question per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/take_exam.html', {
        'quiz': quiz,
        'course': course,
        'attempt': attempt,
        'page_obj': page_obj,  # Pass the paginated questions to the template
    })

@login_required
def submit_exam(request, attempt_id):
    # Fetch the user’s quiz attempt
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)

    # Redirect if the quiz has already been completed
    if attempt.completed:
        return redirect('student_dashboard')

    # Initialize score
    score = 0
    for question in attempt.quiz.questions.all():
        selected_choice_id = request.POST.get(f"question_{question.id}")
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            is_correct = selected_choice.is_correct
            if is_correct:
                score += question.marks  # Add marks for correct answers
            # Save the user's answer
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                choice=selected_choice,
                is_correct=is_correct
            )

    # Mark the quiz as completed and save the score
    attempt.completed = True
    attempt.completed_at = timezone.now()
    attempt.score = score
    attempt.save()

    # Redirect to the exam results page
    return redirect('exam_results', attempt_id=attempt.id)


@login_required
def exam_results(request, attempt_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)

    if not attempt.completed:
        # Handle case where the exam is not completed yet
        return redirect('take_exam', course_id=attempt.quiz.course.id)

    # Prepare the data to be passed to the template
    score = attempt.score
    quiz = attempt.quiz

    # Fetch the user's answers
    user_answers = UserAnswer.objects.filter(attempt=attempt)

    return render(request, 'student/exam_results.html', {
        'score': score,
        'quiz': quiz,
        'user_answers': user_answers
    })


def calculate_feedback(percentage):
    """
    Returns feedback based on the user's percentage.
    """
    if percentage >= 90:
        return "Excellent work! You have a great understanding of the material."
    elif 75 <= percentage < 90:
        return "Good job! You performed well, but there's room for improvement."
    elif 50 <= percentage < 75:
        return "You passed, but consider reviewing the material to strengthen your understanding."
    elif 30 <= percentage < 50:
        return "Below average. It's important to revisit the material and try again."
    else:
        return "Poor performance. Please go through the material thoroughly and seek help if needed."

@login_required
@user_passes_test(is_teacher_admin_or_student)
def view_results(request, attempt_id):
    """
    Displays the results of a completed quiz attempt, records the marks, and tracks all attempts.
    """
    # Fetch the user's quiz attempt and ensure it belongs to the logged-in user
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)

    # Redirect if the attempt is incomplete
    if not attempt.completed:
        messages.error(request, "You must complete the quiz before viewing results.")
        return redirect('resume_exam', attempt_id=attempt.id)

    # Fetch related quiz and attempt details
    quiz = attempt.quiz
    score = attempt.score

    # Record the score in the history if not already recorded
    if not attempt.recorded:
        attempt.recorded = True
        attempt.save()

        # Log the attempt in a separate history model
        QuizAttemptHistory.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            attempt_date=now()
        )

    # Fetch the user's answers for this attempt with question details
    user_answers = UserAnswer.objects.filter(attempt=attempt).select_related('question')

    # Calculate the total marks for the quiz
    total_marks = sum(user_answer.question.marks for user_answer in user_answers)

    # Prepare a detailed breakdown of each question
    questions = []
    for answer in user_answers:
        questions.append({
            'text': answer.question.question_text,
            'selected_option': answer.selected_option,
            'correct_option': answer.question.correct_option,
            'correct': answer.selected_option == answer.question.correct_option,
            'marks': answer.question.marks,
            'feedback': answer.question.explanation,
        })

    # Calculate the percentage, grade, and feedback
    percentage = (score / total_marks) * 100 if total_marks > 0 else 0
    grade = calculate_grade(score, total_marks)
    feedback = calculate_feedback(percentage)

    # Fetch all attempts for this quiz
    attempt_history = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-score')

    # Count the total number of attempts
    total_attempts = attempt_history.count()

    # Fetch leaderboard data for the quiz (if available)
    leaderboard = Leaderboard.objects.filter(quiz=quiz).order_by('-score') if Leaderboard.objects.filter(quiz=quiz).exists() else None

    # Pass data to the template
    return render(request, 'student/view_results.html', {
        'attempt': attempt,           # Current attempt object
        'quiz': quiz,                 # Quiz object
        'score': score,               # Final score
        'max_score': total_marks,     # Total marks for the quiz
        'percentage': percentage,     # Percentage score
        'grade': grade,               # Calculated grade
        'feedback': feedback,         # Feedback based on performance
        'questions': questions,       # Detailed question data
        'attempt_history': attempt_history,  # User's attempt history
        'total_attempts': total_attempts,    # Total number of attempts
        'leaderboard': leaderboard,   # Leaderboard data (optional)
    })








def error_page(request):
    return render(request, 'student/error_page.html')
#
# # Check if user is a student
# def is_student(user):
#     return user.groups.filter(name='STUDENT').exists()
#
# # User role check for student
# def is_student(user):
#     return user.role == 'student'


@login_required
@user_passes_test(is_teacher_admin_or_student)
def student_dashboard_view(request):
    student = Student.objects.get(user_id=request.user.id)

    # Display the total number of courses, quizzes, and questions available
    context = {
        'total_courses': Course.objects.all().count(),
        'total_quizzes': Quiz.objects.all().count(),
        'total_questions': Question.objects.all().count(),
    }
    return render(request, 'student/dashboard.html', context)


@login_required
@user_passes_test(is_teacher_admin_or_student)
def student_exam_view(request):
    # Show available quizzes
    quizzes = Quiz.objects.all()  # Fetch all quizzes from the database
    return render(request, 'student_exam.html', {'quizzes': quizzes})


@login_required
@user_passes_test(is_teacher_admin_or_student)
def take_exam_view(request, pk):
    # Fetch the quiz
    quiz = get_object_or_404(Quiz, id=pk)

    # Check if the quiz has no questions, and redirect if true
    if quiz.questions.count() == 0:  # Assuming a related name `questions` exists
        messages.error(request, "This quiz has no questions available.")
        return redirect('student-exam')  # Redirect to the student exam page

    # Initialize or reset the quiz attempt for the user
    user = request.user
    quiz_attempt, created = UserQuizAttempt.objects.get_or_create(
        user=user,
        quiz=quiz,
        completed=False,
        recorded=False,  # Ensures it hasn't been recorded yet
        defaults={'started_at': timezone.now(), 'score': 0},  # Set default score as 0
    )

    if not created:  # If an attempt already exists and is still incomplete, reset it
        quiz_attempt.score = 0  # Reset score if necessary
        quiz_attempt.completed = False  # Mark as incomplete
        quiz_attempt.started_at = timezone.now()  # Reset start time
        quiz_attempt.completed_at = None  # Reset completion time
        quiz_attempt.save()

    # Check if the attempt is completed already
    if quiz_attempt.completed:
        messages.info(request, "You have already completed this quiz.")
        return redirect('quiz_results', pk=quiz.pk)

    # Handle the form submission or answer updates
    if request.method == 'POST':
        # Assume answers are submitted in a dictionary (question_id -> selected_option)
        selected_answers = request.POST.getlist('answers')  # List of selected options

        # For each answer, save the result and calculate the score
        score = 0
        for question, selected_option in zip(quiz.questions.all(), selected_answers):
            is_correct = question.correct_option == selected_option
            UserAnswer.objects.create(
                attempt=quiz_attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )
            if is_correct:
                score += question.marks  # Add marks for correct answers

        # Update the quiz attempt with the calculated score
        quiz_attempt.score = score  # Ensure score is updated and not NULL
        quiz_attempt.completed = True  # Mark as completed
        quiz_attempt.completed_at = timezone.now()  # Record completion time
        quiz_attempt.save()

        # Optionally, save to QuizAttemptHistory for tracking historical attempts
        QuizAttemptHistory.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            attempt_date=timezone.now()
        )

        # Optionally, calculate and record the final marks in the Marks model
        student = user.student  # Assuming the user has a related Student model
        if student:
            Marks.objects.create(
                student=student,
                course=quiz.questions.first().course,  # Assuming all questions belong to the same course
                score=score,
                grade='A' if score >= 80 else 'B',  # Example grade calculation
            )

        # Redirect to results page
        return redirect('quiz_results', pk=quiz.pk)

    return render(request, 'take_exam.html', {'quiz': quiz, 'quiz_attempt': quiz_attempt})


@login_required
@user_passes_test(is_teacher_admin_or_student)
def quiz_transcript_view(request):
    user = request.user

    # Fetch all quiz attempts for the logged-in user
    quiz_attempts = UserQuizAttempt.objects.filter(user=user, completed=True)

    # Prepare a summary of attempts and calculate total score and total max score
    attempts_summary = []
    total_score = 0
    total_max_score = 0

    for attempt in quiz_attempts:
        # Fetch user answers related to the current attempt
        user_answers = UserAnswer.objects.filter(attempt=attempt)

        # Calculate the total marks by summing individual question marks
        total_marks = sum(user_answer.question.marks for user_answer in user_answers)  # Summing question marks

        # Update total score and total max score
        total_score += attempt.score
        total_max_score += total_marks

        # Append attempt details to the summary
        attempts_summary.append({
            'quiz': attempt.quiz,  # Pass the entire quiz object to be used in the template
            'score': attempt.score,
            'max_score': total_marks,  # Dynamically calculated total marks
            'percentage': (attempt.score / total_marks) * 100 if total_marks > 0 else 0,
            'completed_at': attempt.completed_at,
            'grade': calculate_grade(attempt.score, total_marks),  # Grade calculation logic
        })

    # Calculate the average percentage if total_max_score > 0
    average_percentage = (total_score / total_max_score) * 100 if total_max_score > 0 else 0

    # Calculate the average grade based on the average percentage
    average_grade = calculate_grade(average_percentage, 100)  # Calculate average grade based on percentage

    context = {
        'attempts_summary': attempts_summary,
        'average_percentage': average_percentage,
        'average_grade': average_grade,
        'total_score':total_score,
        'total_max_score':total_max_score
    }

    return render(request, 'quiz_transcript.html', context)


def calculate_grade(score, max_score):
    """Helper function to calculate grade based on score percentage."""
    if max_score == 0:
        return 'N/A'
    percentage = (score / max_score) * 100
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'



@login_required
@user_passes_test(is_teacher_admin_or_student)
def start_exam_view(request, quiz_id):
    # Fetch the quiz and its related questions
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions_in_quiz.all()

    # Check if the quiz has questions
    if not questions.exists():
        messages.error(request, "This quiz has no questions available.")
        return redirect('student-exam')  # Assuming 'student-exam' is defined in urls.py

    # If the request is POST, process the quiz attempt
    if request.method == 'POST':
        # Check if the user already has an ongoing or completed attempt for this quiz
        user_attempts = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz)

        if 'clear_all' in request.POST:
            # Clear all attempts
            user_attempts.delete()
            messages.success(request, "All your attempts have been cleared.")
            return redirect('student-exam')  # Redirect to the exam list page or dashboard

        if 'clear_failed' in request.POST:
            # Clear failed attempts only
            failed_attempts = user_attempts.filter(completed=False)
            failed_attempts.delete()
            messages.success(request, "All failed attempts have been cleared.")
            return redirect('student-exam')

        # Check if the user has any ongoing attempts
        ongoing_attempt = user_attempts.filter(completed=False).first()

        if ongoing_attempt:
            user_attempt = ongoing_attempt
        else:
            # No ongoing attempts, create a new one
            user_attempt = UserQuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                completed=False,
                score=0,
                started_at=timezone.now()  # Set the start time when the quiz starts
            )

        # Process the answers
        total_score = 0
        for question in questions:
            # Retrieve the selected option from the POST data
            selected_option = request.POST.get(f"question_{question.id}")

            if selected_option:
                # Check if the selected option is the correct answer
                is_correct = selected_option == question.correct_option

                # Calculate score increment
                if is_correct:
                    total_score += question.marks

                # Save the user's answer
                UserAnswer.objects.create(
                    attempt=user_attempt,
                    question=question,
                    selected_option=selected_option,  # This must match the UserAnswer model field
                    is_correct=is_correct
                )

        # Update and complete the quiz attempt
        user_attempt.score = total_score
        user_attempt.completed = True
        user_attempt.completed_at = timezone.now()  # Set the end time when the quiz is completed
        user_attempt.save()

        # Redirect to the results or a confirmation page
        return redirect('view_results', attempt_id=user_attempt.id)

    # Render the exam page
    return render(request, 'start_exam.html', {'quiz': quiz, 'questions': questions})

@login_required
@user_passes_test(is_teacher_admin_or_student)
def calculate_marks_view(request):
    if request.COOKIES.get('quiz_id') is not None:
        quiz_id = request.COOKIES.get('quiz_id')
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.all()

        total_marks = 0
        for i, question in enumerate(questions):
            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = question.correct_option
            if selected_ans == actual_answer:
                total_marks += question.marks

        student = Student.objects.get(user_id=request.user.id)

        # Save the result to the Marks model
        result = Marks(student=student, course=quiz.course, score=total_marks, grade='A' if total_marks >= 50 else 'B',
                       date_taken=timezone.now())
        result.save()

        return HttpResponseRedirect(reverse('view-result'))


@login_required
@user_passes_test(is_teacher_admin_or_student)
def view_result_view(request):
    try:
        # Fetch the student object based on the logged-in user
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        raise Http404("Student not found")

    # Fetch the student's marks/results from the Marks table
    results = Marks.objects.filter(student=student)

    # Fetch the student's answers (if applicable)
    # Assuming the Answer model was meant to be UserAnswer based on the models provided
    answers = UserAnswer.objects.filter(attempt__user=student.user)

    # Prepare the context data to be passed to the template
    context = {
        'results': results,  # The student's results
        'answers': answers,  # The student's answers
    }

    # Render the results and answers to the 'view_result.html' template
    return render(request, 'view_result.html', context)

#@login_required
@user_passes_test(is_teacher_admin_or_student)
def check_marks_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    student = Student.objects.get(user_id=request.user.id)
    results = Marks.objects.filter(quiz=quiz, student=student)
    return render(request, 'check_marks.html', {'results': results})


#@login_required
@user_passes_test(is_teacher_admin_or_student)
def student_marks_view(request):
    # Show all quizzes taken by the student
    student = Student.objects.get(user_id=request.user.id)
    marks = Marks.objects.filter(student=student)
    return render(request, 'student_marks.html', {'marks': marks})


def assign_exam(request):
    if request.method == 'POST':
        form = AssignExamForm(request.POST)
        if form.is_valid():
            # Save the form (assign the exam)
            assigned_exam = form.save()

            # Optionally, you can access the assigned exam and student here for additional logic
            student = assigned_exam.student  # Assuming `AssignExamForm` has a 'student' field

            # Show success message
            messages.success(request, 'Exam assigned successfully!')

            # Redirect to the student exam view after successful assignment
            return redirect('student-exam')  # Redirecting to the view where the student can take the exam

        else:
            messages.error(request, 'Failed to assign exam.')
    else:
        form = AssignExamForm()

    return render(request, 'assign_exam.html', {'form': form})


def teacher_or_admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')  # Redirect to login page if the user is not authenticated

        # Check if the user is a teacher or admin
        if request.user.role not in ['teacher', 'admin']:
            messages.error(request, "You do not have permission to view this page.")
            return redirect('home')  # Redirect to home if not a teacher or admin

        return view_func(request, *args, **kwargs)

    return _wrapped_view


# Manage Questions
@login_required
@teacher_or_admin_required
def manage_questions(request):
    questions = Question.objects.all()
    return render(request, 'teacher/manage_questions.html', {'questions': questions})


@login_required
#@teacher_or_admin_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_questions')
    else:
        form = QuestionForm()

    return render(request, 'teacher/add_question.html', {'form': form, 'exam': request.GET.get('exam', None)})

@login_required
@teacher_or_admin_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('manage_questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'teacher/update_question.html', {'form': form})

@login_required
@teacher_or_admin_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('manage_questions')

# Manage Quizzes (Exams)
@login_required
@teacher_or_admin_required
def manage_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'teacher/manage_quizzes.html', {'quizzes': quizzes})

@login_required
@teacher_or_admin_required
def add_quiz(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = ExamForm()
    return render(request, 'teacher/add_quiz.html', {'form': form})

@login_required
@teacher_or_admin_required
def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = ExamForm(instance=quiz)
    return render(request, 'teacher/update_quiz.html', {'form': form})

@login_required
@teacher_or_admin_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect('manage_quizzes')



# Reset all quiz attempts for a user
def reset_all_quizzes(request):
    user = request.user
    attempts = UserQuizAttempt.objects.filter(user=user)

    # Reset the quizzes
    attempts.update(score=0, completed=False, completed_at=None, recorded=False)

    messages.success(request, "All quizzes have been reset.")
    return redirect('quiz_transcript')


@login_required
@user_passes_test(is_teacher_admin_or_student)
def reset_quiz(request, quiz_id):
    user = request.user
    attempt = UserQuizAttempt.objects.filter(user=user, quiz_id=quiz_id).first()

    if attempt:
        # Reset the quiz attempt data
        attempt.score = 0
        attempt.completed = False
        attempt.completed_at = None
        attempt.recorded = False
        attempt.save()

        # Success message
        messages.success(request, f"Quiz '{attempt.quiz.title}' has been reset.")
    else:
        # Error message if attempt is not found
        messages.error(request, "Quiz attempt not found.")

    # Redirect to the quiz transcript page after resetting
    return redirect('quiz_transcript')


def testimonials_view(request):
    # Fetch all testimonials from the database
    testimonials = Testimonial.objects.all()

    return render(request, 'home.html', {'testimonials': testimonials})
