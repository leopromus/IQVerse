from datetime import date
from django.utils import timezone
from quiz.models import User, Teacher, Student, Course, Question, Quiz

# Create Users
user1 = User.objects.create_user(username="john_doe", email="john@example.com", password="password", role="teacher")
user2 = User.objects.create_user(username="jane_doe", email="jane@example.com", password="password", role="student")

# Create a Teacher
teacher = Teacher.objects.create(
    user=user1,
    subject="Physics",
    is_approved=True,
    experience=5,
    qualification="Master's Degree in Physics",
    bio="Experienced Physics teacher from Kigali.",
    phone_number="+250788123456"
)

# Create Students
student1 = Student.objects.create(
    user=user2,
    grade="Senior 5",
    date_of_birth=date(2007, 5, 12),
    phone_number="+250788654321",
    parent_contact="+250788987654"
)

# Create Course
course = Course.objects.create(
    teacher=teacher,
    title="Advanced Physics",
    description="A course on advanced physics concepts and their applications.",
    category="Science",
    difficulty_level="intermediate",
    duration=12  # 12 weeks
)

# Create Quizzes
quiz1 = Quiz.objects.create(
    title="Kinematics Quiz",
    description="A quiz on basic kinematics concepts.",
    time_limit=30  # 30 minutes
)

quiz2 = Quiz.objects.create(
    title="Electricity Quiz",
    description="A quiz on basic electricity concepts.",
    time_limit=45  # 45 minutes
)

# Create Questions
Question.objects.create(
    quiz=quiz1,
    course=course,
    question_text="What is the formula for velocity?",
    option1="v = d/t",
    option2="v = m/a",
    option3="v = F/m",
    option4="v = a*t",
    correct_option="1",
    question_type="multiple_choice",
    marks=5
)

Question.objects.create(
    quiz=quiz1,
    course=course,
    question_text="What is the SI unit of speed?",
    option1="Meter",
    option2="Second",
    option3="Meter per second",
    option4="Kilometer",
    correct_option="3",
    question_type="multiple_choice",
    marks=5
)

Question.objects.create(
    quiz=quiz2,
    course=course,
    question_text="What is the unit of electric current?",
    option1="Volt",
    option2="Ohm",
    option3="Coulomb",
    option4="Ampere",
    correct_option="4",
    question_type="multiple_choice",
    marks=5
)

Question.objects.create(
    quiz=quiz2,
    course=course,
    question_text="What is the formula for electric power?",
    option1="P = V/I",
    option2="P = V*I",
    option3="P = I/R",
    option4="P = V*R",
    correct_option="2",
    question_type="multiple_choice",
    marks=5
)

# Create Additional Data for Diversity
student2 = User.objects.create_user(username="alice_rwanda", email="alice@example.com", password="password", role="student")
student3 = User.objects.create_user(username="eric_kiny", email="eric@example.com", password="password", role="student")
Student.objects.create(user=student2, grade="Senior 4", date_of_birth=date(2008, 8, 25), phone_number="+250788332211")
Student.objects.create(user=student3, grade="Senior 6", date_of_birth=date(2006, 3, 18), phone_number="+250788776655")

print("Database populated successfully!")











from quiz.models import Question, Quiz, Course

# Assume quiz and course are pre-existing
quiz = Quiz.objects.get(id=1)  # Example quiz id
course = Course.objects.get(id=1)  # Example course id

for q in question1:
    Question.objects.create(
        quiz=quiz,
        course=course,
        question_text=q["question_text"],
        option1=q["option1"],
        option2=q["option2"],
        option3=q["option3"],
        option4=q["option4"],
        correct_option=q["correct_option"],
        question_type=q["question_type"],
        explanation=q["explanation"],
        marks=q["marks"]
    )




question1 = [
    {
        "question_text": "What is the speed of light in a vacuum?",
        "option1": "3.00 × 10^6 m/s",
        "option2": "3.00 × 10^8 m/s",
        "option3": "1.00 × 10^8 m/s",
        "option4": "1.00 × 10^9 m/s",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The speed of light in a vacuum is approximately 3.00 × 10^8 meters per second.",
        "marks": 5
    },
    {
        "question_text": "What is the value of Planck’s constant?",
        "option1": "6.626 × 10^-34 J·s",
        "option2": "3.141 × 10^-34 J·s",
        "option3": "9.109 × 10^-31 J·s",
        "option4": "1.602 × 10^-19 J·s",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "Planck's constant is 6.626 × 10^-34 J·s, a fundamental constant in quantum mechanics.",
        "marks": 5
    },
    {
        "question_text": "What is the energy of a photon with a wavelength of 500 nm?",
        "option1": "3.97 × 10^-19 J",
        "option2": "4.00 × 10^-19 J",
        "option3": "2.50 × 10^-19 J",
        "option4": "5.00 × 10^-19 J",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The energy of a photon is calculated by E = hc/λ, where h is Planck's constant, c is the speed of light, and λ is the wavelength.",
        "marks": 5
    },
    {
        "question_text": "What is the wavelength of an electron moving with a velocity of 3.0 × 10^6 m/s? (h = 6.626 × 10^-34 J·s)",
        "option1": "2.42 × 10^-10 m",
        "option2": "1.33 × 10^-10 m",
        "option3": "5.55 × 10^-10 m",
        "option4": "8.94 × 10^-10 m",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The de Broglie wavelength of an electron is λ = h / mv. Substituting the values, we get λ = 2.42 × 10^-10 m.",
        "marks": 5
    },
    {
        "question_text": "What is the electric field strength at a point 2 meters from a charge of 5 μC?",
        "option1": "9.0 × 10^9 N/C",
        "option2": "1.8 × 10^3 N/C",
        "option3": "2.0 × 10^9 N/C",
        "option4": "2.2 × 10^9 N/C",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The electric field strength is given by E = kQ / r^2. Using the value of Coulomb’s constant (k = 9.0 × 10^9 N·m²/C²), we get E = 1.8 × 10^3 N/C.",
        "marks": 5
    },
    {
        "question_text": "What is the total energy of a system consisting of a 2-kg mass at a height of 10 m above the ground? (g = 9.8 m/s²)",
        "option1": "196 J",
        "option2": "200 J",
        "option3": "150 J",
        "option4": "300 J",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The potential energy (PE) is given by PE = mgh. Substituting the values, PE = 2 × 9.8 × 10 = 196 J.",
        "marks": 5
    },
    {
        "question_text": "What is the period of a pendulum with a length of 1.0 m? (g = 9.8 m/s²)",
        "option1": "1.0 s",
        "option2": "2.0 s",
        "option3": "3.2 s",
        "option4": "4.0 s",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The period of a simple pendulum is given by T = 2π√(L/g). For L = 1.0 m, T = 2π√(1/9.8) ≈ 2.0 s.",
        "marks": 5
    },
    {
        "question_text": "What is the momentum of a 5-kg object moving at a speed of 3 m/s?",
        "option1": "15 kg·m/s",
        "option2": "10 kg·m/s",
        "option3": "12 kg·m/s",
        "option4": "5 kg·m/s",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "Momentum is given by p = mv. For a 5-kg object moving at 3 m/s, p = 5 × 3 = 15 kg·m/s.",
        "marks": 5
    },
    {
        "question_text": "What is the value of the gravitational constant G?",
        "option1": "6.674 × 10^-11 N·m²/kg²",
        "option2": "9.8 × 10^9 N·m²/kg²",
        "option3": "6.022 × 10^-23 N·m²/kg²",
        "option4": "9.8 × 10^-11 N·m²/kg²",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The gravitational constant is G = 6.674 × 10^-11 N·m²/kg².",
        "marks": 5
    },
    {
        "question_text": "What is the temperature in Celsius at which the Kelvin scale starts?",
        "option1": "0°C",
        "option2": "100°C",
        "option3": "-273°C",
        "option4": "273°C",
        "correct_option": "3",
        "question_type": "multiple_choice",
        "explanation": "The Kelvin scale starts at absolute zero, which is -273°C.",
        "marks": 5
    },
    {
        "question_text": "What is the work done when a force of 10 N moves an object 5 meters?",
        "option1": "50 J",
        "option2": "20 J",
        "option3": "30 J",
        "option4": "15 J",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "Work done is given by W = F × d. For F = 10 N and d = 5 m, W = 10 × 5 = 50 J.",
        "marks": 5
    },
    {
        "question_text": "What is the charge on an electron?",
        "option1": "1.6 × 10^-19 C",
        "option2": "1.6 × 10^-18 C",
        "option3": "-1.6 × 10^-19 C",
        "option4": "-1.6 × 10^-18 C",
        "correct_option": "3",
        "question_type": "multiple_choice",
        "explanation": "The charge on an electron is -1.6 × 10^-19 C.",
        "marks": 5
    },
    {
        "question_text": "Which law explains the relationship between the current and voltage in an ideal conductor?",
        "option1": "Newton's law",
        "option2": "Ohm's law",
        "option3": "Coulomb's law",
        "option4": "Faraday's law",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "Ohm's law states that the current through a conductor is directly proportional to the voltage across it, provided the temperature is constant.",
        "marks": 5
    },
    {
        "question_text": "What is the primary force responsible for the motion of planets in orbit?",
        "option1": "Electromagnetic force",
        "option2": "Gravitational force",
        "option3": "Nuclear force",
        "option4": "Frictional force",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "The primary force responsible for the motion of planets in orbit is gravitational force, as described by Newton's law of gravitation.",
        "marks": 5
    },
    {
        "question_text": "What is the formula for the kinetic energy of an object?",
        "option1": "KE = 1/2 mv^2",
        "option2": "KE = mv^2",
        "option3": "KE = mgh",
        "option4": "KE = 1/2 mgh",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The formula for kinetic energy is KE = 1/2 mv^2, where m is mass and v is velocity.",
        "marks": 5
    },
    {
        "question_text": "What is the primary particle responsible for beta radiation?",
        "option1": "Alpha particle",
        "option2": "Beta particle",
        "option3": "Neutron",
        "option4": "Proton",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "Beta radiation consists of high-energy, high-speed electrons or positrons, also known as beta particles.",
        "marks": 5
    },
    {
        "question_text": "What is the phenomenon called when light bends as it passes from one medium to another?",
        "option1": "Reflection",
        "option2": "Refraction",
        "option3": "Diffraction",
        "option4": "Dispersion",
        "correct_option": "2",
        "question_type": "multiple_choice",
        "explanation": "Refraction is the bending of light as it passes from one medium to another, due to a change in its speed.",
        "marks": 5
    },
    {
        "question_text": "What is the formula for the gravitational force between two objects?",
        "option1": "F = G(m1m2)/r²",
        "option2": "F = G(m1m2)/r",
        "option3": "F = Gm1m2r",
        "option4": "F = G(m1m2)r²",
        "correct_option": "1",
        "question_type": "multiple_choice",
        "explanation": "The formula for the gravitational force is F = G(m1m2)/r², where G is the gravitational constant, m1 and m2 are the masses of the objects, and r is the distance between them.",
        "marks": 5
    }



]






from quiz.models import Quiz, Course, Question

# Assume you already have a Quiz object and a Course object
quiz = Quiz.objects.get(title="Advanced Mathematics Quiz")
course = Course.objects.get(title="Advanced Mathematics")

# Create the questions
questions = [
    Question(
        quiz=quiz,
        course=course,
        question_text="Evaluate the integral: ∫(3x^2 + 2x - 5) dx",
        option1="x^3 + x^2 - 5x + C",
        option2="x^3 + x^2 + 5x + C",
        option3="x^3 + x - 5x + C",
        option4="3x^2 + 2x - 5 + C",
        correct_option="1",
        question_type="multiple_choice",
        explanation="The integral of 3x^2 is x^3, the integral of 2x is x^2, and the integral of -5 is -5x. Add the constant of integration, C.",
        marks=5,
    ),
    Question(
        quiz=quiz,
        course=course,
        question_text="What is the determinant of the matrix [[2, -3], [4, 5]]?",
        option1="10",
        option2="-10",
        option3="20",
        option4="15",
        correct_option="2",
        question_type="multiple_choice",
        explanation="The determinant is calculated as (2*5) - (4*-3) = 10 - (-12) = -10.",
        marks=5,
    ),
    Question(
        quiz=quiz,
        course=course,
        question_text="Find the eigenvalues of the matrix [[3, 1], [0, 2]].",
        option1="3 and 1",
        option2="2 and 0",
        option3="3 and 2",
        option4="1 and 0",
        correct_option="3",
        question_type="multiple_choice",
        explanation="The eigenvalues are the diagonal elements of a triangular matrix, which are 3 and 2.",
        marks=5,
    ),
    Question(
        quiz=quiz,
        course=course,
        question_text="If P(A) = 0.6 and P(B) = 0.7, and A and B are independent events, what is P(A ∩ B)?",
        option1="1.3",
        option2="0.6",
        option3="0.7",
        option4="0.42",
        correct_option="4",
        question_type="multiple_choice",
        explanation="For independent events, P(A ∩ B) = P(A) * P(B) = 0.6 * 0.7 = 0.42.",
        marks=5,
    ),
    Question(
        quiz=quiz,
        course=course,
        question_text="Solve the equation: x^3 - 3x^2 + 4 = 0",
        option1="x = 1, x = 2",
        option2="x = -1, x = 2",
        option3="x = -1, x = 3",
        option4="x = 1, x = -2",
        correct_option="2",
        question_type="multiple_choice",
        explanation="Using factorization, x^3 - 3x^2 + 4 = 0 factors into (x+1)(x-2)^2 = 0. The solutions are x = -1 and x = 2.",
        marks=5,
    ),
]

# Save the questions to the database
for question in questions:
    question.save()

print("Advanced Mathematics questions have been added successfully.")









