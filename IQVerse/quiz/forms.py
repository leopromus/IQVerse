from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Teacher, Student, TeacherApplication, Course, Question


# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']


# Teacher Signup Form
class TeacherSignupForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        teacher = Teacher.objects.create(user=user, subject=self.cleaned_data['subject'])
        return teacher


# Student Signup Form
class StudentSignupForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    grade = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        student = Student.objects.create(user=user, grade=self.cleaned_data['grade'])
        return student


class TeacherApplicationForm(forms.ModelForm):
    """
    Form for users to apply as a teacher.
    """
    class Meta:
        model = TeacherApplication
        fields = ['full_name', 'email', 'resume', 'cover_letter']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your cover letter here...',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'resume': 'Upload Resume (PDF only)',
            'cover_letter': 'Cover Letter',
        }

    def clean_resume(self):
        """
        Validate that the uploaded resume is a PDF.
        """
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed for resumes.')
        return resume

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course Description', 'rows': 4}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Course title must be at least 5 characters long.")
        return title


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'marks']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the question text'}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 1'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 2'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 3'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option 4'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Marks for this question'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], attrs={'class': 'form-control'})
        }

    def clean_correct_option(self):
        correct_option = self.cleaned_data.get('correct_option')
        if correct_option not in [1, 2, 3, 4]:
            raise forms.ValidationError("Invalid option for correct answer. It must be between 1 and 4.")
        return correct_option



# Teacher Form
class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    is_approved = forms.BooleanField(required=False)
    subject = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Teacher
        fields = ['is_approved', 'subject']

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        teacher = super(TeacherForm, self).save(commit=False)
        user = teacher.user

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            teacher.save()
        return teacher


# Student Form
class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    grade = forms.CharField(max_length=10, required=True)

    class Meta:
        model = Student
        fields = ['grade']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        student = super(StudentForm, self).save(commit=False)
        user = student.user

        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            student.save()
        return student

