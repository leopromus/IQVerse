from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum

from .decorators import teacher_or_admin_required
from .forms import TeacherSignupForm, StudentSignupForm, CourseForm, QuestionForm, TeacherForm, StudentForm
from .models import Marks, Teacher, Student, Course, Question, TeacherApplication
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Course, Question, Marks


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeacherApplication  # Assuming the model is TeacherApplication
from .forms import TeacherApplicationForm  # Assuming the form is TeacherApplicationForm



# Automatically assign a user to the 'Teacher' group when a Teacher instance is created
@receiver(post_save, sender=Teacher)
def add_teacher_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Teacher')
        instance.user.groups.add(group)

# Automatically assign a user to the 'Student' group when a Student instance is created
@receiver(post_save, sender=Student)
def add_student_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Student')
        instance.user.groups.add(group)



def home(request):
    return render(request, 'home.html')


# def redirect_to_dashboard(user):
#     """Redirect users to their specific dashboards based on roles."""
#     if user.is_superuser:
#         return redirect(reverse('admin_dashboard'))
#     elif user.groups.filter(name='Teacher').exists():
#         return redirect(reverse('teacher_dashboard'))
#     elif user.groups.filter(name='Student').exists():
#         return redirect(reverse('student_dashboard'))
#     else:
#         return redirect(reverse('home'))


# Login View


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Assign to selected group
        group = Group.objects.get(name=role)
        user.groups.add(group)

        messages.success(request, f"Account created successfully! You are registered as a {role}.")
        return redirect('login')

    return render(request, 'registration/signup.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Admin').exists():
                return '/quiz/admin/dashboard/'  # Adjust if you have a custom admin dashboard
            elif user.groups.filter(name='Teacher').exists():
                return '/quiz/teacher-dashboard/'
            elif user.groups.filter(name='Student').exists():
                return '/quiz/student-dashboard/'
        return super().get_success_url()


def logout_view(request):
    logout(request)
    return redirect('login')


# Teacher Signup
def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Teacher.objects.create(user=user)
            messages.success(request, "Teacher registered successfully!")
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = TeacherSignupForm()
    return render(request, 'teacher_signup.html', {'form': form})


# Student Signup
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            messages.success(request, "Student registered successfully!")
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})


# Dashboard View for Admin
@login_required
@permission_required('quiz.view_admin_dashboard', raise_exception=True)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_questions = Question.objects.count()
    teachers = Teacher.objects.all()

    context = {
        'user': request.user,
        'teachers': teachers,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_questions': total_questions
    }

    return render(request, 'admin_dashboard.html', context)

# Approve Teacher

@staff_member_required
def approve_teacher(request, teacher_id):
    """
    Approve a teacher application by admin/staff.
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        teacher.approved = True
        teacher.save()
        return redirect('teacher_dashboard')  # Redirect to the teacher's dashboard

    return render(request, 'approve_teacher.html', {'teacher': teacher})

@staff_member_required
def pending_teachers(request):
    """
    List all pending teacher applications for approval.
    """
    pending_teachers = Teacher.objects.filter(approved=False)
    return render(request, 'pending_teachers.html', {'pending_teachers': pending_teachers})



def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def approve_teacher_application(request, application_id):
    application = get_object_or_404(TeacherApplication, id=application_id)
    if not application.approved:
        application.approved = True
        application.save()
        # Notify user
        send_mail(
            'Your Application is Approved',
            f'Dear {application.user.username}, your teacher application has been approved.',
            'admin@example.com',
            [application.user.email],
            fail_silently=False,
        )
        messages.success(request, "Application approved and notification sent.")
    return redirect('admin:quiz_teacherapplication_changelist')


# Update Teacher
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully!")
            return redirect('update_teacher')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'update_teacher.html', {'form': form})


# Delete Teacher
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully!")
        return redirect('delete_teacher')
    return render(request, 'delete_teacher.html', {'teacher': teacher})

# Update Student
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('update_student')
    else:
        form = StudentForm(instance=student)
    return render(request, 'update_student.html', {'form': form})


# Delete Student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('delete_student')
    return render(request, 'delete_student.html', {'student': student})


# View Marks
def view_marks(request):
    students = Student.objects.all()
    return render(request, 'view_marks.html', {'students': students})




# CRUD for Teacher
@login_required
def manage_teacher(request, teacher_id=None):
    teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None

    if request.method == "POST":
        username = request.POST.get('username')
        subject = request.POST.get('subject')
        if teacher:
            teacher.user.username = username
            teacher.subject = subject
            teacher.save()
            messages.success(request, f"Teacher {teacher.user.username} updated successfully!")
        else:
            user = User.objects.create_user(username=username, password='temporarypassword')
            teacher = Teacher.objects.create(user=user, subject=subject)
            messages.success(request, f"Teacher {teacher.user.username} created successfully!")
        return redirect('admin_dashboard')

    context = {'teacher': teacher}
    return render(request, 'manage_teacher.html', context)


# CRUD for Student
@login_required
def manage_student(request, student_id=None):
    student = Student.objects.get(id=student_id) if student_id else None

    if request.method == "POST":
        username = request.POST.get('username')
        grade = request.POST.get('grade')
        if student:
            student.user.username = username
            student.grade = grade
            student.save()
            messages.success(request, f"Student {student.user.username} updated successfully!")
        else:
            user = User.objects.create_user(username=username, password='temporarypassword')
            student = Student.objects.create(user=user, grade=grade)
            messages.success(request, f"Student {student.user.username} created successfully!")
        return redirect('admin_dashboard')

    context = {'student': student}
    return render(request, 'manage_student.html', context)


# Add/Delete/View Course
@login_required
@teacher_or_admin_required
def manage_course(request, course_id=None):
    course = Course.objects.get(id=course_id) if course_id else None

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        teacher_id = request.POST.get('teacher')
        teacher = Teacher.objects.get(id=teacher_id)
        if course:
            course.title = title
            course.description = description
            course.teacher = teacher
            course.save()
            messages.success(request, f"Course {course.title} updated successfully!")
        else:
            course = Course.objects.create(title=title, description=description, teacher=teacher)
            messages.success(request, f"Course {course.title} created successfully!")
        return redirect('admin_dashboard')

    teachers = Teacher.objects.all()
    context = {'course': course, 'teachers': teachers}
    return render(request, 'manage_course.html', context)




# Add/View/Delete Questions
@login_required
def manage_question(request, question_id=None):
    question = Question.objects.get(id=question_id) if question_id else None

    if request.method == "POST":
        course_id = request.POST.get('course')
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = request.POST.get('correct_option')
        marks = request.POST.get('marks')
        course = Course.objects.get(id=course_id)

        if question:
            question.course = course
            question.question_text = question_text
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.correct_option = correct_option
            question.marks = marks
            question.save()
            messages.success(request, "Question updated successfully!")
        else:
            Question.objects.create(course=course, question_text=question_text,
                                    option1=option1, option2=option2, option3=option3,
                                    option4=option4, correct_option=correct_option, marks=marks)
            messages.success(request, "Question added successfully!")
        return redirect('admin_dashboard')

    courses = Course.objects.all()
    context = {'question': question, 'courses': courses}
    return render(request, 'manage_question.html', context)


# Teacher Dashboard

# Check if the user is a teacher
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

# Check if the user is a student
def is_student(user):
    return user.groups.filter(name='Student').exists()


@permission_required('quiz.add_teacher', raise_exception=True)
def add_teacher(request):
    # Your logic to add a teacher
    pass

# @login_required
# @permission_required('quiz.change_teacher', raise_exception=True)
# def approve_teacher(request, teacher_id):
#     teacher = Teacher.objects.get(id=teacher_id)
#     teacher.status = 'Approved'
#     teacher.save()
#     return redirect('admin_dashboard')


@login_required
def teacher_dashboard(request):
    """
    Handle teacher dashboard access:
    - Existing teachers are redirected to their dashboard.
    - Approved teacher applications are processed and added to the Teacher model.
    - Unapproved applications are redirected to the application status page.
    - Users without an application are redirected to apply.
    """
    try:
        # Check if the user is already a teacher
        teacher = Teacher.objects.get(user=request.user)
        # Redirect existing teachers directly to the dashboard
        return render(request, 'teacher_dashboard.html', {
            'total_courses': Course.objects.filter(teacher=teacher).count(),
            'total_questions': Question.objects.filter(course__teacher=teacher).count(),
            'courses': Course.objects.filter(teacher=teacher),
            'questions': Question.objects.filter(course__teacher=teacher),
        })

    except Teacher.DoesNotExist:
        # Check if the user has applied to become a teacher
        try:
            teacher_application = TeacherApplication.objects.get(user=request.user)

            if teacher_application.approved:
                # Create a new teacher instance if the application is approved
                Teacher.objects.create(
                    user=request.user,
                    subject="Subject Not Specified"
                )
                return redirect('teacher_dashboard')
            else:
                # Redirect to application status if not yet approved
                return redirect('teacher_application_status')

        except TeacherApplication.DoesNotExist:
            # Redirect to application page if no application exists
            return redirect('teacher_apply')


# Student-only view
@login_required
#@permission_required('quiz.view_student_dashboard', raise_exception=True)

def student_dashboard(request):
    # Get the student's associated user object
    student = get_object_or_404(Student, user=request.user)

    # Get total courses, total questions, total attempts, and total marks
    total_courses = Course.objects.count()
    total_questions = Question.objects.count()
    total_attempts = Marks.objects.filter(student=student).count()

    # Calculate the total marks for the student; return 0 if no marks are found
    total_marks = Marks.objects.filter(student=student).aggregate(total=Sum('score'))['total'] or 0

    # Fetch all courses that the student is enrolled in (assuming relationship exists)
    courses = Course.objects.all()  # You can filter this to the student's enrolled courses if needed

    # Prepare context to pass to the template
    context = {
        'student': student,
        'total_courses': total_courses,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'total_marks': total_marks,
        'courses': courses,  # Pass the list of courses to the template
    }

    return render(request, 'student_dashboard.html', context)


@login_required
def take_exam(request, course_id):
    # Get the course by ID or return a 404 error if not found
    course = get_object_or_404(Course, id=course_id)

    # Get the questions related to this course
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':
        total_score = 0

        # Loop through the questions to check the selected options and calculate the score
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option and int(selected_option) == question.correct_option:
                total_score += question.marks

        # Save the total score in the Marks table
        Marks.objects.create(student=request.user.student, course=course, score=total_score)

        # Redirect to view_marks to show the result
        return redirect('view_marks')

    context = {'course': course, 'questions': questions}
    return render(request, 'take_exam.html', context)


@login_required
def view_marks(request, student_id=None):
    """
    Admins can view marks for any student by providing `student_id`.
    Students can view only their own marks.
    """
    # Check if the user is an admin or student
    if request.user.is_staff:  # Admin Access
        if student_id:
            # Admin viewing a specific student's marks
            student = get_object_or_404(Student, id=student_id)
            marks = Marks.objects.filter(student=student).order_by('-date_taken')
        else:
            # Admin viewing all student marks
            marks = Marks.objects.all().order_by('-date_taken')
            student = None  # No specific student to show
    else:  # Student Access
        try:
            # Regular student viewing their own marks
            student = Student.objects.get(user=request.user)
            marks = Marks.objects.filter(student=student).order_by('-date_taken')
        except Student.DoesNotExist:
            messages.error(request, "You are not registered as a student.")
            return redirect('home')  # Redirect non-student users to home/dashboard

    context = {
        'marks': marks,
        'student': student,
    }
    return render(request, 'view_marks.html', context)


# Exam Guidelines
@login_required
def exam_guidelines(request):
    return render(request, 'exam_guidelines.html')


def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        # You can use a form or a simple model update depending on your needs.
        # Assuming the user is a student, but you can check if the user is a teacher as well.
        try:
            student_profile = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student_profile = None

        # If you're editing a teacher profile, you can get teacher data here
        try:
            teacher_profile = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            teacher_profile = None

        context = {
            'student_profile': student_profile,
            'teacher_profile': teacher_profile,
        }

        return render(request, 'edit_profile.html', context)

    else:
        return redirect('login')  # Redirect to login page if not authenticated


@login_required
def teacher_apply(request):
    """
    View for teacher application form submission.
    """
    if request.method == 'POST':
        form = TeacherApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('teacher_application_status')  # Redirect after successful submission
    else:
        form = TeacherApplicationForm()

    return render(request, 'teacher_apply.html', {'form': form})


@login_required
def teacher_application_status(request):
    """
    Display the status of the teacher application.
    """
    try:
        teacher_application = TeacherApplication.objects.get(user=request.user)
    except TeacherApplication.DoesNotExist:
        return redirect('teacher_apply')  # If no application exists, redirect to application page

    context = {
        'teacher_application': teacher_application,
    }
    return render(request, 'teacher_application_status.html', context)


@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new course
            messages.success(request, 'Course added successfully!')
            return redirect('teacher_dashboard')  # Redirect to the teacher dashboard
        else:
            # Debugging - log form errors
            print(form.errors)  # Print form errors to the console for debugging
            messages.error(request, 'There was an error while adding the course. Please try again.')
    else:
        form = CourseForm()  # Initialize the form for GET request

    return render(request, 'add_course.html', {'form': form})


def view_courses(request):
    courses = Course.objects.all()  # Assuming you have a Course model
    return render(request, 'view_courses.html', {'courses': courses})


def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('teacher_dashboard')
    return render(request, 'delete_course.html', {'course': course})


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question added successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Error adding question. Please try again.')
    else:
        form = QuestionForm()

    return render(request, 'add_question.html', {'form': form})

def view_questions(request):
    questions = Question.objects.all()  # Assuming you have a Question model
    return render(request, 'view_questions.html', {'questions': questions})

def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('teacher_dashboard')
    return render(request, 'delete_question.html', {'question': question})
