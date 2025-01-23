## Project Overview

The **Interactive Quiz Platform** is a web application built with **Django** that allows users to take quizzes, manage quiz content, and track performance. It supports teachers creating and managing quizzes, students taking quizzes, and administrators overseeing the platform.

# **Key Features**

* **User Roles**: Teachers, Students, Admins with distinct permissions.
* **Quiz Management**: Teachers can create, update, and delete quizzes.
* **Student Interaction**: Students can attempt quizzes, check scores, and provide feedback.
* **Leaderboards**: Track top performers for each quiz.
* **Teacher Applications**: Admins can approve teachers to create quizzes.
* **Course & Exam Management**: Organize quizzes into courses with difficulty levels.


# Technologies Used

* **Django**: Web framework for backend development.
* **Mysql**: Database for development (replaceable with PostgreSQL or MySQL for production).
* **HTML/CSS**: Frontend for a clean UI.
* **Bootstrap**: For responsive design.
* **Python 3**: Backend programming language.

# Installation


```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/interactive-quiz-platform.git
cd interactive-quiz-platform

# Step 2: Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Apply migrations
python manage.py migrate

# Step 5: Create a superuser
python manage.py createsuperuser

# Step 6: Run the server
python manage.py runserver

```

# **project structure**


```plaintext
IQVerse/
├── manage.py             # Django management script
├── IQVerse/              # Main project folder
│   ├── __init__.py       # Project initialization
├── quiz/                 # Main app folder
│   
│   ├── templates/        # HTML templates
│   ├── static/           # Static files (CSS, JS)
│       ├── css/          # CSS files
│       ├── js/           # JavaScript files
│   ├── migrations/       # Database migrations
│       ├── __init__.py   # Migrations initialization
├── requirements.txt      # Project dependencies
├── Mysql                 # Mysql database (development)
└── README.md             # Project documentation
```

# **contributors**

`Twayinganyiki Promis Leonce` - Project owner and lead developer


# **license**

under `Alx/Sandbox` tech