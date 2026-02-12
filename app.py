import os
from flask import Flask, render_template, session
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
=======
@app.route('/')
def about_page():
    return render_template('about.html')

@app.route('/')
def rules_page():
    return render_template('rules.html')

>>>>>>> 3f555bb8b60fc46a7f9539ac120a93386b6ae938
@app.route('/new_game')
def new_game_page():
    words = db.session.query(Word).filter_by(is_available=1).all() # hämtar alla tillgängliga ord

    if not words: # safeguard ifall det är slut på ord
        return render_template('new_game.html', word=None) # none hanteras i new_game.html
    
    word = random.choice(words) # ansätter randomly ett av dessa till "word(of the day)"
    word.is_available=False
    db.session.commit()
    return render_template('new_game.html', word=word) # skickar med word till new_game

# Temporär logik för new_game med sessions [som är dictionary-liknande objekt]
# @app.route('/new_game')
# def new_game_page():

<<<<<<< HEAD
>>>>>>> d8b8e1ac2568884812a1e0fc7b8269ca59bcd31d
if __name__ == "__main__":
    app.run(debug=True)
=======
#     # vi kollar först om ett spel redan pågår
#     if "word_id" in session: # word_id är en "nyckel" i session som korresponderar mot den INT som är PK i Words-tabellen
#         word = Word.query.get(session["word_id"]) # och kan därför hämta ordet från databasen
#         return render_template('new_game.html', word=word)
    
#     # annars startar vi ett nytt spel
#     words = db.session.query(Word).filter_by(is_available = True).all()

#     # om det inte finns ord (p.g.a. t.ex. slut) skickar vi None så får det hanteras i jinja
#     if not words:
#         return render_template('new_game.html', word = None)
    
#     # slumpa ett ord av listan med ord vi gjorde query ifrån
#     word = random.choice(words)
#     word.is_available = False # <- ansätt samma ord till 'unavailable'
#     db.session.commit() # och uppdatera databasen

#     # spara valt ord i session, men flask sessions kan bara spara enkla datatyper (int, str)
#     session["word_id"] = word.id # sessionen för ordet får bli PK för det valda ordet
#     session["attempts"] = 0 # sätt antalet gissningar till 0

#     return render_template('new_game.html', word=word)

#     # sedan måste vi skapa routes från formulären från new_game som "poppar" sessionen när spelet är slut
#     # eller uppdaterar antalet gissningar vid gissningar


if __name__ == "__main__":    
>>>>>>> 3f555bb8b60fc46a7f9539ac120a93386b6ae938
    with app.app_context():
        seedData() 
    app.run(debug=True)
