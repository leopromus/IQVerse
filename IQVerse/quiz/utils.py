# utils.py

def calculate_quiz_score(quiz, correct_answers, total_questions):
    """
    Calculates the score for a quiz based on the correct answers.

    :param quiz: The Quiz object the student is attempting
    :param correct_answers: The number of correct answers the student gave
    :param total_questions: Total number of questions in the quiz
    :return: The calculated score as a percentage
    """
    if total_questions == 0:
        return 0  # Avoid division by zero if there are no questions

    score = (correct_answers / total_questions) * 100
    return score
