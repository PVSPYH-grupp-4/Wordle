import os
from flask import Flask, render_template
from seed import seedData
from database import db
from dotenv import load_dotenv
from flask_migrate import Migrate
<<<<<<< HEAD
from forms import GuessForm
=======
from model import Word
import random
>>>>>>> d8b8e1ac2568884812a1e0fc7b8269ca59bcd31d

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
db.init_app(app)
migrate= Migrate(app, db)

# render to main page
@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD

#guess

@app.route("/", methods=["GET", "POST"])
def index():
    form = GuessForm()

    if form.validate_on_submit():
        guess = form.guess.data.lower()
        print("User guess:", guess)  # later: compare with the secret word

    return render_template("index.html", form=form)
=======
@app.route('/new_game')
def new_game_page():
    words = db.session.query(Word).filter_by(is_available=1).all() # hämtar alla tillgängliga ord

    if not words: # safeguard ifall det är slut på ord
        return render_template('new_game.html', word=None) # none hanteras i new_game.html
    
    word = random.choice(words) # ansätter randomly ett av dessa till "word(of the day)"
    word.is_available=False
    db.session.commit()
    return render_template('new_game.html', word=word) # skickar med word till new_game


>>>>>>> d8b8e1ac2568884812a1e0fc7b8269ca59bcd31d
if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        seedData()