from .models import User, TeacherApplication, Question, Course, Student, Settings, Teacher, Quiz
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.forms.widgets import HiddenInput
# forms.py
from django import forms
from .models import StudentExam
from django.contrib.auth import get_user_model



class UserForm(forms.ModelForm):
    # Adding two password fields for confirmation
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    # Custom validator to ensure passwords match
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    # Add role choices manually if you have specific roles (you can modify this based on your project)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # Adding placeholders for other fields
            if field_name == 'username':
                field.widget.attrs.update({'placeholder': 'Enter your username'})
            elif field_name == 'email':
                field.widget.attrs.update({'placeholder': 'Enter your email'})
            elif field_name == 'role':
                field.widget.attrs.update({'placeholder': 'Select your role'})

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
    )

    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']


class TeacherApplicationForm(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        fields = ['full_name', 'email', 'phone_number', 'resume', 'cover_letter']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'difficulty_level', 'duration', 'teacher']

    # Customize teacher field to show available teachers for admins
    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')  # Get the current user from the view
        super().__init__(*args, **kwargs)
        if user and user.role == 'admin':
            # Admin can select from all teachers
            self.fields['teacher'].queryset = Teacher.objects.all()
        elif user and user.role == 'teacher':
            # Teacher's own teacher is pre-selected and hidden
            self.fields['teacher'].queryset = Teacher.objects.filter(user=user)
            self.fields['teacher'].widget = forms.HiddenInput()  # Hide the teacher field for teachers


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option',
                  'question_type', 'explanation', 'marks']

    def __init__(self, *args, **kwargs):
        # Extract request object if passed
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            if request.user.role == 'teacher':
                # Filter courses based on the teacher's scope
                self.fields['course'].queryset = Course.objects.filter(teacher=request.user.teacher)
            else:
                # Admin can see all courses
                self.fields['course'].queryset = Course.objects.all()

    def save(self, commit=True):
        # Save the form but attach the quiz to the question before saving
        question = super().save(commit=False)

        # If exam (quiz) is provided, associate the question with the exam
        if 'exam' in self.data:
            exam = self.data.get('exam')
            question.quiz = Quiz.objects.get(id=exam)

        if commit:
            question.save()
        return question


class StudentForm(forms.ModelForm):
    # We do not need to directly use 'user' in a ModelChoiceField here.
    # Instead, you can set it properly via the foreign key relation in the view.
    # Hence, we’ll remove the user selection field and let it be handled by the view logic.
    # You can still display it if necessary using a custom widget, but it's better to handle
    # the relation between the student and user via the view.

    class Meta:
        model = Student
        fields = ['grade', 'date_of_birth', 'phone_number', 'parent_contact', 'profile_image']

    # Add any custom logic if necessary (e.g., setting 'user' automatically in the view)
    # Optionally, you can keep the field for displaying, but it's already handled via the model's relationship.


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['site_name', 'email', 'description', 'contact_number', 'logo', 'facebook_url', 'twitter_url', 'instagram_url']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit', 'questions']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quiz Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Quiz Description'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Time Limit in Minutes'}),
            'questions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Quiz Title',
            'description': 'Description',
            'time_limit': 'Time Limit (Minutes)',
            'questions': 'Select Questions',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the queryset for the questions field
        self.fields['questions'].queryset = Question.objects.all()


class AssignExamForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['student', 'exam']

    student = forms.ModelChoiceField(queryset=get_user_model().objects.filter(role='student'), required=True)
    exam = forms.ModelChoiceField(queryset=Quiz.objects.all(), required=True)

