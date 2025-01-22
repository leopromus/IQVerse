from datetime import date, timedelta
from django.utils.timezone import now
from quiz.models import (
    User, Teacher, Student, Course, Question, Marks, TeacherApplication,
    Quiz, Choice, UserQuizAttempt, UserAnswer, Feedback, Leaderboard
)

# Clear existing data
User.objects.all().delete()
Teacher.objects.all().delete()
Student.objects.all().delete()
Course.objects.all().delete()
Question.objects.all().delete()
Marks.objects.all().delete()
TeacherApplication.objects.all().delete()
Quiz.objects.all().delete()
Choice.objects.all().delete()
UserQuizAttempt.objects.all().delete()
UserAnswer.objects.all().delete()
Feedback.objects.all().delete()
Leaderboard.objects.all().delete()

# Create users
teacher_user = User.objects.create_user(username="karangwa", email="karangwa@example.com", password="teacher123", role="teacher")
student_user1 = User.objects.create_user(username="mukamisha", email="mukamisha@example.com", password="student123", role="student")
student_user2 = User.objects.create_user(username="ndayisenga", email="ndayisenga@example.com", password="student123", role="student")

admin_user = User.objects.create_superuser(
    username="mukandoli",
    email="mukandoli.admin@example.com",
    password="admin123",
    role="admin"
)

# Creating teacher users
teacher1_user = User.objects.create_user(
    username="manirakiza",
    email="manirakiza@example.com",
    password="teacher123",
    role="teacher"
)

teacher2_user = User.objects.create_user(
    username="rukundo",
    email="rukundo@example.com",
    password="teacher123",
    role="teacher"
)

# Adding teacher-specific details
teacher1 = Teacher.objects.create(
    user=teacher1_user,
    subject="Mathematics",
    experience=5,
    qualification="M.Ed. in Mathematics",
    bio="Passionate about teaching and shaping future leaders.",
    phone_number="+250780123456"
)

teacher2 = Teacher.objects.create(
    user=teacher2_user,
    subject="Biology",
    experience=3,
    qualification="M.Sc. in Biology",
    bio="Dedicated to making biology simple and fun.",
    phone_number="+250781654321"
)

# Creating student users
student1_user = User.objects.create_user(
    username="umwali",
    email="umwali@example.com",
    password="student123",
    role="student"
)

student2_user = User.objects.create_user(
    username="nyiranziza",
    email="nyiranziza@example.com",
    password="student123",
    role="student"
)

# Adding student-specific details
student1 = Student.objects.create(
    user=student1_user,
    grade="Grade 10",
    date_of_birth=date(2006, 5, 15),
    phone_number="+250789123456",
    parent_contact="+250788654321"
)

student2 = Student.objects.create(
    user=student2_user,
    grade="Grade 12",
    date_of_birth=date(2005, 8, 22),
    phone_number="+250788123654",
    parent_contact="+250787321456"
)



# Create teachers
teacher = Teacher.objects.create(
    user=teacher_user,
    subject="Mathematics",
    is_approved=True,
    experience=10,
    qualification="Master's in Mathematics",
    bio="Passionate about teaching mathematics.",
    phone_number="0781234567"
)

# Create students
student1 = Student.objects.create(
    user=student_user1,
    grade="P6",
    date_of_birth=date(2008, 5, 15),
    phone_number="0789876543",
    parent_contact="0787654321"
)
student2 = Student.objects.create(
    user=student_user2,
    grade="S3",
    date_of_birth=date(2006, 11, 23),
    phone_number="0781122334",
    parent_contact="0789988776"
)

# Create courses
course1 = Course.objects.create(
    teacher=teacher,
    title="Algebra Basics",
    description="An introductory course on algebraic principles.",
    category="Mathematics",
    difficulty_level="beginner",
    duration=4
)
course2 = Course.objects.create(
    teacher=teacher,
    title="Geometry for Beginners",
    description="Learn the basics of geometry.",
    category="Mathematics",
    difficulty_level="beginner",
    duration=6
)

# Create questions
question1 = Question.objects.create(
    course=course1,
    question_text="What is the value of x in the equation 2x + 3 = 7?",
    option1="1",
    option2="2",
    option3="3",
    option4="4",
    correct_option="2",
    question_type="multiple_choice",
    marks=5
)
question2 = Question.objects.create(
    course=course2,
    question_text="What is the sum of the angles in a triangle?",
    option1="90",
    option2="180",
    option3="360",
    option4="None of the above",
    correct_option="2",
    question_type="multiple_choice",
    marks=5
)

# Create marks
Marks.objects.create(student=student1, course=course1, score=85.0, grade="A", feedback="Excellent work!")
Marks.objects.create(student=student2, course=course2, score=75.0, grade="B", feedback="Good effort.")

# Create teacher applications
TeacherApplication.objects.create(
    user=teacher_user,
    full_name="Karangwa Jean",
    email="karangwa@example.com",
    phone_number="0781234567",
    cover_letter="I am passionate about teaching and sharing knowledge.",
    approved=True
)

# Create quizzes
quiz1 = Quiz.objects.create(title="Algebra Quiz", description="Test your algebra skills.", time_limit=20)

# Create choices
Choice.objects.create(question=question1, text="1", is_correct=False)
Choice.objects.create(question=question1, text="2", is_correct=True)
Choice.objects.create(question=question1, text="3", is_correct=False)
Choice.objects.create(question=question1, text="4", is_correct=False)

# Create user quiz attempts
attempt1 = UserQuizAttempt.objects.create(
    user=student_user1,
    quiz=quiz1,
    score=90.0,
    completed=True,
    started_at=now() - timedelta(minutes=30),
    completed_at=now()
)

# Create user answers
UserAnswer.objects.create(attempt=attempt1, question=question1, choice=Choice.objects.get(question=question1, text="2"), is_correct=True)

# Create feedback
Feedback.objects.create(attempt=attempt1, feedback_text="Great attempt!")

# Create leaderboard
Leaderboard.objects.create(quiz=quiz1, user=student_user1, score=90.0)

























from django.contrib.auth.models import User
from quiz.models import Teacher, Student

# Create Admin user
admin_user = User.objects.create_superuser(username="admin_rwanda", password="admin123", email="admin@example.com", role="admin")
admin_user.save()

# Create Teacher users with Rwandan names
teacher1_user = User.objects.create_user(username="kamanzi_jean", password="teacher123", email="kamanzi.jean@example.com", role="teacher")
teacher1_user.save()

teacher2_user = User.objects.create_user(username="mugisha_sandra", password="teacher123", email="mugisha.sandra@example.com", role="teacher")
teacher2_user.save()

# Create Student users with Rwandan names
student1_user = User.objects.create_user(username="munezero_ruth", password="student123", email="munezero.ruth@example.com", role="student")
student1_user.save()

student2_user = User.objects.create_user(username="ngendahimana_peter", password="student123", email="ngendahimana.peter@example.com", role="student")
student2_user.save()

# Add Teacher profiles
teacher1 = Teacher.objects.create(user=teacher1_user, subject="Mathematics", experience=10, is_approved=True)
teacher2 = Teacher.objects.create(user=teacher2_user, subject="Physics", experience=8, is_approved=True)

# Add Student profiles
student1 = Student.objects.create(user=student1_user, grade="10", date_of_birth="2005-05-15")
student2 = Student.objects.create(user=student2_user, grade="10", date_of_birth="2005-07-20")

# Assuming teacher instances and courses for physics and English are already populated










from django.contrib.auth.models import User
from quiz.models import Teacher, Student



# Example physics and English courses
physics_course = Course.objects.get(title="Physics")
english_course = Course.objects.get(title="English")

# List of advanced-level physics and English questions
questions_data = [
    # Physics Questions
    {
        'course': physics_course,
        'question_text': 'What is the value of Planck\'s constant?',
        'option1': '6.626 × 10^-34 J·s',
        'option2': '3.141 × 10^-34 J·s',
        'option3': '1.602 × 10^-19 J·s',
        'option4': '9.81 m/s²',
        'correct_option': '1',
        'question_type': 'multiple_choice',
        'explanation': 'Planck\'s constant is 6.626 × 10^-34 J·s, which is a fundamental constant in quantum mechanics.',
        'marks': 5
    },
    {
        'course': physics_course,
        'question_text': 'What is the Schrödinger equation used for in quantum mechanics?',
        'option1': 'Describing the wave function of a quantum system',
        'option2': 'Calculating gravitational force',
        'option3': 'Solving Maxwell\'s equations',
        'option4': 'Finding the speed of light in a vacuum',
        'correct_option': '1',
        'question_type': 'multiple_choice',
        'explanation': 'The Schrödinger equation describes how the quantum state of a physical system changes over time.',
        'marks': 5
    },
    {
        'course': physics_course,
        'question_text': 'Which particle is responsible for the strong nuclear force?',
        'option1': 'Proton',
        'option2': 'Neutron',
        'option3': 'Photon',
        'option4': 'Gluon',
        'correct_option': '4',
        'question_type': 'multiple_choice',
        'explanation': 'The strong nuclear force is mediated by gluons, which bind quarks together to form protons and neutrons.',
        'marks': 5
    },
    # Add more physics questions here...

    # English Questions
    {
        'course': english_course,
        'question_text': 'What is the main theme of Shakespeare\'s play "Macbeth"?',
        'option1': 'The rise and fall of ambition',
        'option2': 'The quest for knowledge',
        'option3': 'The power of love',
        'option4': 'The conflict between good and evil',
        'correct_option': '1',
        'question_type': 'multiple_choice',
        'explanation': 'The main theme of "Macbeth" is the rise and fall of ambition, as Macbeth\'s desire for power leads to his downfall.',
        'marks': 5
    },
    {
        'course': english_course,
        'question_text': 'Which literary device is used in the phrase "the wind whispered through the trees"?',
        'option1': 'Alliteration',
        'option2': 'Metaphor',
        'option3': 'Personification',
        'option4': 'Simile',
        'correct_option': '3',
        'question_type': 'multiple_choice',
        'explanation': 'Personification is used when human characteristics are attributed to non-human things, as seen in "the wind whispered".',
        'marks': 5
    },
    {
        'course': english_course,
        'question_text': 'What is the function of a semicolon in English grammar?',
        'option1': 'To separate two independent clauses closely related in meaning',
        'option2': 'To end a sentence',
        'option3': 'To separate items in a list',
        'option4': 'To indicate a question',
        'correct_option': '1',
        'question_type': 'multiple_choice',
        'explanation': 'A semicolon is used to separate two independent clauses that are closely related in meaning.',
        'marks': 5
    },
    # Add more English questions here...
]

# Insert the questions into the database
for question in questions_data:
    Question.objects.create(
        course=question['course'],
        question_text=question['question_text'],
        option1=question['option1'],
        option2=question['option2'],
        option3=question['option3'],
        option4=question['option4'],
        correct_option=question['correct_option'],
        question_type=question['question_type'],
        explanation=question['explanation'],
        marks=question['marks']
    )













advanced_geography_questions = [
    {
        "question_text": "Which country is home to the Atacama Desert, the driest non-polar desert in the world?",
        "option1": "Peru",
        "option2": "Chile",
        "option3": "Bolivia",
        "option4": "Argentina",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The Atacama Desert is located in northern Chile and is known for its extreme aridity.",
        "marks": 5
    },
    {
        "question_text": "What is the deepest point in the Earth's oceans?",
        "option1": "Java Trench",
        "option2": "Puerto Rico Trench",
        "option3": "Mariana Trench",
        "option4": "Tonga Trench",
        "correct_option": "3",
        "question_type": "multiple_choice",
        "explanation": "The Mariana Trench, specifically the Challenger Deep, is the deepest point in the world's oceans.",
        "marks": 5
    },
    {
        "question_text": "Which river has the largest drainage basin in the world?",
        "option1": "Amazon River",
        "option2": "Nile River",
        "option3": "Congo River",
        "option4": "Mississippi River",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The Amazon River has the largest drainage basin, covering about 7 million square kilometers.",
        "marks": 5
    },
    {
        "question_text": "What is the largest active volcano in the world by volume?",
        "option1": "Mauna Loa",
        "option2": "Mount Etna",
        "option3": "Krakatoa",
        "option4": "Mount St. Helens",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "Mauna Loa, located in Hawaii, is the world's largest active volcano by volume.",
        "marks": 5
    },
    {
        "question_text": "Which country has the highest number of neighboring countries (land borders)?",
        "option1": "Russia",
        "option2": "China",
        "option3": "Brazil",
        "option4": "Germany",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "China has 14 neighboring countries, sharing the highest count along with Russia.",
        "marks": 5
    },
    {
        "question_text": "What is the primary cause of the Aurora Borealis (Northern Lights)?",
        "option1": "Solar wind particles colliding with Earth's magnetic field",
        "option2": "Volcanic eruptions",
        "option3": "Earth's rotation",
        "option4": "Cloud condensation at high altitudes",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The Aurora Borealis occurs when solar wind particles collide with gases in Earth's atmosphere.",
        "marks": 5
    },
    {
        "question_text": "Which ocean current is known as the 'Global Conveyor Belt'?",
        "option1": "Gulf Stream",
        "option2": "Thermohaline Circulation",
        "option3": "Kuroshio Current",
        "option4": "Agulhas Current",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The Thermohaline Circulation is a global system of deep and surface currents, often referred to as the 'Global Conveyor Belt.'",
        "marks": 5
    },
    {
        "question_text": "What is the largest lake in Africa by surface area?",
        "option1": "Lake Tanganyika",
        "option2": "Lake Victoria",
        "option3": "Lake Malawi",
        "option4": "Lake Chad",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "Lake Victoria is the largest lake in Africa by surface area and the second-largest freshwater lake in the world.",
        "marks": 5
    },
    {
        "question_text": "Which continent has the most countries?",
        "option1": "Asia",
        "option2": "Africa",
        "option3": "Europe",
        "option4": "South America",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "Africa has 54 recognized countries, making it the continent with the most countries.",
        "marks": 5
    },
    {
        "question_text": "What is the name of the region where tectonic plates meet, often associated with frequent earthquakes and volcanic activity?",
        "option1": "Mid-Atlantic Ridge",
        "option2": "Pacific Ring of Fire",
        "option3": "San Andreas Fault",
        "option4": "Great Rift Valley",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The Pacific Ring of Fire is a horseshoe-shaped region with intense tectonic activity, including earthquakes and volcanoes.",
        "marks": 5
    }
]








