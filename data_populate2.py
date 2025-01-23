from datetime import date, timedelta
from django.utils.timezone import now
from quiz.models import (
    User, Teacher, Student, Course, Question, Marks, TeacherApplication,
    Quiz, Choice, UserQuizAttempt, UserAnswer, Feedback, Leaderboard
)
# Creating an admin user
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





from datetime import datetime
from quiz.models import Teacher, Course, Question, Quiz

# Assuming the teacher and courses are already created
teacher = Teacher.objects.get(id=1)  # Replace with the actual teacher ID

# Create Chemistry and Biology Courses for the Teacher
chemistry_course = Course.objects.create(
    teacher=teacher,
    title="Advanced Chemistry",
    description="In-depth study of chemical reactions, molecular structure, and organic chemistry.",
    category="Chemistry",
    difficulty_level="advanced",
    duration=12
)

biology_course = Course.objects.create(
    teacher=teacher,
    title="Advanced Biology",
    description="Exploring genetics, microbiology, evolution, and physiology at an advanced level.",
    category="Biology",
    difficulty_level="advanced",
    duration=12
)

# Create the Chemistry and Biology Quizzes
chemistry_quiz = Quiz.objects.create(course=chemistry_course, title="Advanced Chemistry Quiz")
biology_quiz = Quiz.objects.create(course=biology_course, title="Advanced Biology Quiz")

# Define Chemistry Questions
chemistry_questions = [
    {
        'question_text': "What is the difference between SN1 and SN2 reaction mechanisms?",
        'option1': "SN1 is bimolecular, SN2 is unimolecular", 'option2': "SN1 involves a two-step process, SN2 is one-step",
        'option3': "SN1 occurs only with primary carbons, SN2 with tertiary carbons", 'option4': "SN1 forms a transition state, SN2 does not",
        'correct_option': '2', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "SN1 is a two-step process involving a carbocation intermediate, while SN2 is a one-step, bimolecular reaction."
    },
    {
        'question_text': "Which of the following is the most important factor influencing the rate of a reaction according to collision theory?",
        'option1': "Surface area", 'option2': "Temperature", 'option3': "Concentration of reactants", 'option4': "Nature of reactants",
        'correct_option': '2', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "According to collision theory, the rate of reaction increases with temperature, as particles collide more frequently and with higher energy."
    },
    {
        'question_text': "In the reaction 2H₂ + O₂ → 2H₂O, what is the stoichiometric coefficient of oxygen?",
        'option1': "1", 'option2': "2", 'option3': "3", 'option4': "4",
        'correct_option': '2', 'marks': 3, 'question_type': 'multiple_choice',
        'explanation': "The stoichiometric coefficient of oxygen (O₂) is 1 in the balanced reaction."
    },
    {
        'question_text': "Which of the following metals is most likely to undergo corrosion in moist air?",
        'option1': "Iron", 'option2': "Gold", 'option3': "Platinum", 'option4': "Copper",
        'correct_option': '1', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "Iron is the metal most likely to undergo corrosion (rusting) in moist air due to its reaction with oxygen and water."
    },
    {
        'question_text': "What is the principle behind chromatography for separating mixtures?",
        'option1': "Absorption", 'option2': "Solubility", 'option3': "Volatility", 'option4': "Polarity",
        'correct_option': '4', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Chromatography separates mixtures based on differences in polarity, with more polar substances traveling slower."
    },
    {
        'question_text': "Which organic compound has the highest boiling point among the following?",
        'option1': "Methane", 'option2': "Ethanol", 'option3': "Propane", 'option4': "Butane",
        'correct_option': '2', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "Ethanol has the highest boiling point due to hydrogen bonding between molecules, compared to the other non-polar compounds."
    },
    {
        'question_text': "Which of the following statements about the atomic orbitals is true?",
        'option1': "The s orbital is spherical", 'option2': "The p orbital is spherical", 'option3': "The d orbital is spherical", 'option4': "The f orbital is cylindrical",
        'correct_option': '1', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "The s orbital is spherical in shape, while p, d, and f orbitals have more complex geometries."
    },
    {
        'question_text': "Which of the following is the correct description of an endothermic reaction?",
        'option1': "It absorbs heat from its surroundings", 'option2': "It releases heat to its surroundings",
        'option3': "It produces energy in the form of light", 'option4': "It produces a gas as a byproduct",
        'correct_option': '1', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Endothermic reactions absorb heat from the surroundings, leading to a temperature drop in the environment."
    },
    {
        'question_text': "What is the common use of sodium hydroxide in industry?",
        'option1': "Sodium hydroxide is used in soap making", 'option2': "Sodium hydroxide is used in making glass",
        'option3': "Sodium hydroxide is used in the manufacture of synthetic fibers", 'option4': "All of the above",
        'correct_option': '4', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Sodium hydroxide is used in various industrial processes including soap making, glass production, and synthetic fibers."
    },
    {
        'question_text': "In an electrochemical cell, which electrode is considered the cathode?",
        'option1': "The electrode where oxidation occurs", 'option2': "The electrode where reduction occurs",
        'option3': "The electrode connected to the positive terminal", 'option4': "The electrode connected to the negative terminal",
        'correct_option': '2', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "The cathode is the electrode where reduction occurs in an electrochemical cell."
    }
]

# Define Biology Questions
biology_questions = [
    {
        'question_text': "What is the process by which cells generate energy in the absence of oxygen?",
        'option1': "Photosynthesis", 'option2': "Aerobic respiration", 'option3': "Anaerobic respiration", 'option4': "Fermentation",
        'correct_option': '3', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Anaerobic respiration is the process of generating energy without oxygen, typically producing lactic acid or ethanol."
    },
    {
        'question_text': "Which of the following is the key function of DNA polymerase in DNA replication?",
        'option1': "Unwinds the DNA helix", 'option2': "Synthesizes RNA primers", 'option3': "Synthesizes the new DNA strand", 'option4': "Ligates DNA fragments",
        'correct_option': '3', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "DNA polymerase is responsible for synthesizing the new DNA strand during DNA replication."
    },
    {
        'question_text': "What is the primary function of ribosomes in a cell?",
        'option1': "DNA replication", 'option2': "Protein synthesis", 'option3': "Energy production", 'option4': "Cell division",
        'correct_option': '2', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "Ribosomes are the site of protein synthesis in cells."
    },
    {
        'question_text': "What type of mutation occurs when a nucleotide is substituted in the DNA sequence?",
        'option1': "Insertion", 'option2': "Deletion", 'option3': "Substitution", 'option4': "Duplication",
        'correct_option': '3', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "A substitution mutation occurs when a nucleotide is replaced by a different one in the DNA sequence."
    },
    {
        'question_text': "Which of the following is a key difference between prokaryotic and eukaryotic cells?",
        'option1': "Prokaryotic cells lack a cell membrane", 'option2': "Eukaryotic cells lack DNA", 'option3': "Prokaryotic cells lack a nucleus", 'option4': "Eukaryotic cells lack ribosomes",
        'correct_option': '3', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "Prokaryotic cells do not have a membrane-bound nucleus, unlike eukaryotic cells."
    },
    {
        'question_text': "What is the role of the Golgi apparatus in a cell?",
        'option1': "Protein synthesis", 'option2': "Packaging and distribution of proteins", 'option3': "Cell division", 'option4': "DNA replication",
        'correct_option': '2', 'marks': 4, 'question_type': 'multiple_choice',
        'explanation': "The Golgi apparatus is responsible for packaging and distributing proteins and lipids."
    },
    {
        'question_text': "Which structure is responsible for the movement of substances across the cell membrane?",
        'option1': "Mitochondria", 'option2': "Nucleus", 'option3': "Cell membrane channels", 'option4': "Ribosomes",
        'correct_option': '3', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Cell membrane channels facilitate the movement of substances across the cell membrane."
    },
    {
        'question_text': "Which of the following processes is involved in the conversion of glucose to pyruvate?",
        'option1': "Glycolysis", 'option2': "Citric acid cycle", 'option3': "Electron transport chain", 'option4': "Fermentation",
        'correct_option': '1', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Glycolysis is the process of converting glucose into pyruvate in the cytoplasm."
    },
    {
        'question_text': "Which organelle is responsible for the production of ATP?",
        'option1': "Nucleus", 'option2': "Endoplasmic reticulum", 'option3': "Mitochondria", 'option4': "Golgi apparatus",
        'correct_option': '3', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Mitochondria are the powerhouse of the cell, responsible for producing ATP during cellular respiration."
    },
    {
        'question_text': "Which of the following is the main difference between mitosis and meiosis?",
        'option1': "Mitosis results in two genetically identical cells, meiosis results in four genetically distinct cells", 'option2': "Mitosis occurs only in germ cells, meiosis in somatic cells",
        'option3': "Mitosis produces haploid cells, meiosis produces diploid cells", 'option4': "Mitosis involves one division, meiosis involves two",
        'correct_option': '1', 'marks': 5, 'question_type': 'multiple_choice',
        'explanation': "Mitosis results in two genetically identical diploid cells, while meiosis results in four genetically distinct haploid cells."
    }
]

# Create the chemistry questions
for q in chemistry_questions:
    Question.objects.create(
        quiz=chemistry_quiz,
        course=chemistry_course,
        question_text=q['question_text'],
        option1=q['option1'],
        option2=q['option2'],
        option3=q['option3'],
        option4=q['option4'],
        correct_option=q['correct_option'],
        marks=q['marks'],
        question_type=q['question_type'],
        explanation=q['explanation']
    )

# Create the biology questions
for q in biology_questions:
    Question.objects.create(
        quiz=biology_quiz,
        course=biology_course,
        question_text=q['question_text'],
        option1=q['option1'],
        option2=q['option2'],
        option3=q['option3'],
        option4=q['option4'],
        correct_option=q['correct_option'],
        marks=q['marks'],
        question_type=q['question_type'],
        explanation=q['explanation']
    )












from quiz.models import Testimonial,User

# Fetch the existing users (teachers, students, admin)
teacher_gogo = User.objects.get(username='gogo250')
teacher_evariste = User.objects.get(username='evariste')
teacher_karangwa = User.objects.get(username='karangwa')
student_elsa = User.objects.get(username='elsa')
student_rubasha = User.objects.get(username='rubasha')
student_mushi = User.objects.get(username='mushi')
admin_mukandoli = User.objects.get(username='mukandoli')

# Create testimonials
testimonial_1 = Testimonial.objects.create(
    message="The Online Exam System has made teaching more efficient and engaging!",
    user=teacher_gogo,
    role='teacher'
)

testimonial_2 = Testimonial.objects.create(
    message="As a student, I can track my performance easily. The system is amazing!",
    user=student_elsa,
    role='student'
)

testimonial_3 = Testimonial.objects.create(
    message="The system is perfect for managing exams and provides great insights into performance.",
    user=teacher_evariste,
    role='teacher'
)

testimonial_4 = Testimonial.objects.create(
    message="I love the user-friendly interface, and it's so simple to manage my studies!",
    user=student_rubasha,
    role='student'
)

testimonial_5 = Testimonial.objects.create(
    message="Managing the exam system as an admin has never been easier. Great functionality!",
    user=admin_mukandoli,
    role='admin'
)























