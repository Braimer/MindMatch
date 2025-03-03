from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Sample questions
QUESTIONS = [
    {'question': "How many times can you take 2 apples from a pile of 10 apples?",
     'answer': "Once. Then you have a pile of 8 apples.",
     'accept': ['once', 'one', '1']},

    {'question': 'What begins with "e" and ends with "e" but only has one letter in it?',
     'answer': "An envelope.",
     'accept': ['envelope']},

    {'question': "Is it possible to draw a square with three sides?",
     'answer': "Yes. All squares have three sides. They also have a fourth side.",
     'accept': ['yes']}
]

CORRECT_TEXT = ['Correct!', 'That is right.', "You're right.", 'You got it.', 'Righto!']
INCORRECT_TEXT = ['Incorrect!', "Nope, that isn't it.", 'Nope.', 'Not quite.', 'You missed it.']

@app.route('/')
def home():
    session['score'] = 0  # Reset score
    session['current_question'] = 0  # Start from first question
    random.shuffle(QUESTIONS)  # Shuffle questions each time
    session['questions'] = QUESTIONS  # Store shuffled questions
    return redirect(url_for('quiz'))  # Redirect to quiz page

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('result'))  # Redirect to results when done

    question_data = session['questions'][session['current_question']]
    feedback = None

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').lower().strip()

        if user_answer == 'quit':
            return redirect(url_for('result'))

        correct = any(word in user_answer for word in question_data['accept'])
        if correct:
            feedback = random.choice(CORRECT_TEXT)
            session['score'] += 1
        else:
            feedback = f"{random.choice(INCORRECT_TEXT)} The answer is: {question_data['answer']}"

        session['current_question'] += 1

        return render_template('quiz.html', question=question_data, feedback=feedback)

    return render_template('quiz.html', question=question_data)

@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(QUESTIONS)
    return render_template('result.html', score=score, total=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
