from .models import User, TeacherApplication, Question, Course, Student, Settings, Teacher, Quiz
from django.contrib.auth.forms import AuthenticationForm
from .models import StudentExam
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    grade = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Grade"
    )
    parent_contact = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Parent Contact"
    )
    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Subject"
    )
    experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Experience (in years)"
    )
    qualification = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Qualification"
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'role', 'password1', 'password2',
            'grade', 'parent_contact', 'subject', 'experience', 'qualification'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')

        # Password validation
        if password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        # Role-specific validation
        if role == 'student':
            if not cleaned_data.get('grade'):
                self.add_error('grade', 'Grade is required for students.')
            if not cleaned_data.get('parent_contact'):
                self.add_error('parent_contact', 'Parent Contact is required for students.')

        elif role == 'teacher':
            if not cleaned_data.get('subject'):
                self.add_error('subject', 'Subject is required for teachers.')
            if not cleaned_data.get('experience'):
                self.add_error('experience', 'Experience is required for teachers.')
            if not cleaned_data.get('qualification'):
                self.add_error('qualification', 'Qualification is required for teachers.')

        return cleaned_data


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

    def clean(self):
        # Run the base class validation first
        cleaned_data = super().clean()

        # Get the user instance after authentication
        username = cleaned_data.get('username')
        user = self.get_user()

        # Check if the user exists and is authenticated
        if user:
            # Check if the user is a teacher and is not approved
            if user.groups.filter(name='Teacher').exists() and not user.profile.is_approved:
                raise ValidationError(
                    "Your account has not been approved by an admin. Please wait for approval."
                )

        return cleaned_data

    class Meta:
        model = User
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
        fields = ['title', 'description', 'time_limit', 'questions', 'guidelines']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quiz Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Quiz Description'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Time Limit in Minutes'}),
            'questions': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'guidelines': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Guidelines for the Quiz (Separate each guideline with a newline)'}),
        }
        labels = {
            'title': 'Quiz Title',
            'description': 'Description',
            'time_limit': 'Time Limit (Minutes)',
            'questions': 'Select Questions',
            'guidelines': 'Guidelines',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the queryset for the questions field
        self.fields['questions'].queryset = Question.objects.all()

    def clean_guidelines(self):
        # Clean the guidelines and convert them to a bullet-point list
        guidelines = self.cleaned_data.get('guidelines')
        # Split by newline and strip whitespace from each line
        guidelines_list = [line.strip() for line in guidelines.split('\n') if line.strip()]
        return guidelines_list



class AssignExamForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['student', 'exam']

    student = forms.ModelChoiceField(queryset=get_user_model().objects.filter(role='student'), required=True)
    exam = forms.ModelChoiceField(queryset=Quiz.objects.all(), required=True)

