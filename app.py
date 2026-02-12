import os
from flask import Flask, render_template, session
from seed import seedData
from database import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from model import Word
import random

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)
migrate= Migrate(app, db)

# render to main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def about_page():
    return render_template('about.html')

@app.route('/')
def rules_page():
    return render_template('rules.html')

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
    with app.app_context():
        seedData() 
    app.run(debug=True)
