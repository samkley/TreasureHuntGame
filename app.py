from flask import Flask, render_template, request, redirect, url_for, session
import random

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'chickenburger24'

@app.route('/')
def home():
    """Introduction and navigation to the game."""
    # Initialize doubloons to 0 if they are not already set in the session
    if 'doubloons' not in session:
        session['doubloons'] = 0
    return render_template('home.html')

@app.route('/choose-path', methods=['GET', 'POST'])
def choose_path():
    """Let the player choose their path."""
    if request.method == 'POST':
        session['path'] = request.form['path']  # Save the chosen path
        return redirect(url_for('explore'))
    return render_template('choose_path.html')

@app.route('/explore')
def explore():
    """Determine the outcome of the chosen path."""
    path = session.get('path')  # Get the chosen path from the session
    doubloons = session.get('doubloons', 0)  # Default to 0 if not set

    if path == '1':
        outcome = random.choice(['safe', 'trap'])
        if outcome == 'safe':
            session['doubloons'] = doubloons + 100
            result = "You found a treasure chest full of doubloons!"
        else:
            result = "Oh no! A trap was triggered and you barely escaped!"
    elif path == '2':
        outcome = random.choice(['treasure', 'nothing', 'sea monster'])
        if outcome == 'treasure':
            session['doubloons'] = doubloons + 150
            result = "A sparkling pile of doubloons, you're rich!"
        elif outcome == 'nothing':
            result = "An empty cave, better luck next time!"
        else:
            result = "A terrifying sea monster chased you out!"

    return render_template('explore.html', result=result, doubloons=session['doubloons'])

@app.route('/play-again', methods=['POST'])
def play_again():
    """Ask the user if they want to play again or end the game."""
    if 'no' in request.form:
        return redirect(url_for('game_over'))
    return redirect(url_for('choose_path'))

@app.route('/game-over')
def game_over():
    """End of the game screen."""
    doubloons = session.get('doubloons', 0)
    session.clear()  # Reset the session to start fresh next time
    return render_template('game_over.html', doubloons=doubloons)

if __name__ == '__main__':
    app.run(debug=True)
