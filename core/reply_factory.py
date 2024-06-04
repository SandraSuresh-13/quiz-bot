
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.

    if not isinstance(answer, (str, int, float)):
        return False, "Invalid answer type."

    # Store the answer in the session
    if 'answers' not in session:
        session['answers'] = {}

    session['answers'][current_question_id] = answer
    session.modified = True
    '''
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
# Find the index of the current question in the list
    current_index = next((index for (index, d) in enumerate(PYTHON_QUESTION_LIST) if d["id"] == current_question_id), None)

    if current_index is None:
        return "Invalid question ID.", -1

    # Get the next question
    next_index = current_index + 1

    if next_index < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_index]
        return next_question["question"], next_question["id"]
    else:
        return "No more questions.", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    # Retrieve the user's answers from the session
    user_answers = session.get('answers', {})

    # Initialize score
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    # Compare user answers with correct answers
    for question in PYTHON_QUESTION_LIST:
        question_id = question["id"]
        correct_answer = question["answer"]
        user_answer = user_answers.get(question_id, None)

        if user_answer == correct_answer:
            score += 1

    # Calculate percentage score
    percentage_score = (score / total_questions) * 100

    # Generate result message
    result_message = f"You answered {score} out of {total_questions} questions correctly.\n"
    result_message += f"Your score: {percentage_score:.2f}%\n\n"
    result_message += "Detailed results:\n"

    for question in PYTHON_QUESTION_LIST:
        question_id = question["id"]
        question_text = question["question"]
        correct_answer = question["answer"]
        user_answer = user_answers.get(question_id, "No answer provided")

        result_message += f"Question: {question_text}\n"
        result_message += f"Your answer: {user_answer}\n"
        result_message += f"Correct answer: {correct_answer}\n\n"

    return result_message
