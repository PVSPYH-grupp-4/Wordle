import os
from flask import Flask, render_template, session, redirect, url_for, request
from seed import seedData
from database import db
from dotenv import load_dotenv 
from flask_migrate import Migrate
from model import Word
from forms import GuessForm
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

# gammal kod
# @app.route('/new_game')
# def new_game_page():
#     words = db.session.query(Word).filter_by(is_available=1).all() # hämtar alla tillgängliga ord

#     if not words: # safeguard ifall det är slut på ord
#         return render_template('new_game.html', word=None) # none hanteras i new_game.html
    
#     word = random.choice(words) # ansätter randomly ett av dessa till "word(of the day)"
#     word.is_available=False
#     db.session.commit()
#     return render_template('new_game.html', word=word) # skickar med word till new_game

#Temporär logik för new_game med sessions [som är dictionary-liknande objekt]
@app.route('/new_game')
def new_game_page():

    form = GuessForm()

    # vi kollar först om ett spel redan pågår
    if "word_id" in session: # word_id är en "nyckel" i session som korresponderar mot den INT som är PK i Words-tabellen
        word = Word.query.get(session["word_id"]) # och kan därför hämta ordet från databasen
        if not word: # om det av någon anledning inte går att hämta: rensa sessionen
            session.pop("word_id", None)
            session.pop("attempts", None)
            return redirect(url_for("new_game_page")) # skicka tillbaka till new game funktionen
        return render_template('new_game.html', word=word, form=form)
    
    # annars startar vi ett nytt spel
    words = db.session.query(Word).filter_by(is_available = True).all()

    # om det inte finns ord (p.g.a. t.ex. slut) skickar vi None så får det hanteras i jinja
    if not words:
        return render_template('new_game.html', word = None)
    
    # slumpa ett ord av listan med ord vi gjorde query ifrån
    word = random.choice(words)
    word.is_available = False # <- ansätt samma ord till 'unavailable'
    db.session.commit() # och uppdatera databasen

    # spara valt ord i session, men flask sessions kan bara spara enkla datatyper (int, str)
    session["word_id"] = word.id # sessionen för ordet får bli PK för det valda ordet
    session["attempts"] = 0 # sätt antalet gissningar till 0

    return render_template('new_game.html', word=word, form=form)

    # sedan måste vi skapa routes från formulären från new_game som "poppar" sessionen när spelet är slut
    # eller uppdaterar antalet gissningar vid gissningar

@app.route('/guess', methods=['POST'])
def guess():
    
    # om det inte finns ett aktivt spel
    if "word_id" not in session:
        return redirect(url_for("new_game_page"))
    
    # annars hämtar vi ordet från word_id
    word = Word.query.get(session["word_id"])
    if not word: # om det inte går så rensas sessionen
        session.pop("word_id", None)
        session.pop("attempts", None)
        return redirect(url_for("new_game_page"))

 
    # hämtar värdet på det som användaren skrev in (guess) annars returnera ""
    # omvandla värdet till versaler och ta bort blank space
    user_guess = request.form.get("guess", "").strip().upper() 

    # ökar antalet gissningar med 1
    session["attempts"] += 1

    # om användaren gissar rätt: skicka tillbaka "win" till new_game.html
    if user_guess == word.word:
        session.pop("word_id", None)
        session.pop("attempts", None)
        return render_template("new_game.html", word=word, result="win", form=GuessForm())

    # annars, kolla om gissningarna är slut, rensa sessionen och skicka tillbaka "lose"
    if session["attempts"] >= 6:
        session.pop("word_id", None)
        session.pop("attempts", None)
        return render_template("new_game.html", word=word, result="lose", form=GuessForm())

    # annars fortsätter spelet
    return render_template("new_game.html", word=word, result="continue", form=GuessForm())


# # route från new_game som hanterar vad som händer vid gissningar (dvs när man skickar formulär)
# @app.route('/guess', methods=['POST'])
# def guess():
    
#     # om det inte finns ett spel
#     if "word_id" not in session:
#         return redirect(url_for("new_game_page"))
    
#     # annars hämta ordet
#     word = Word.query.get(session["word_id"])
#     if not word:
#         session.pop("word_id", None) # tar bort word_id från sessionen om den finns, annars inget
#         session.pop("attempts", None) # som ovan

#     # Läs användares gissning från formuläret i new_game
#     user_guess = request.form.get("guess", "").strip().upper() # ta bort blanksteg och gör till versaler

#     # antalet försök "ökar" med 1
#     session["attempts"] += 1 # som en dictionary

#     # kollar om det var rätt

#     if user_guess == word.word:
#         result = "win"

#         # tar bort sessionen och spelet avslutas
#         session.pop("word_id", None) 
#         session.pop("attempts", None)
#         return redirect(url_for("new_game.html"))


#     # annars kollar om man gjort alla försk (6)
#     if session["attempts"] >= 6:
#         result = "lose"
#         session.pop("word_id", None)
#         session.pop("attempts", None)

#         return render_template("new_game.html", word=word, result=result)
    
#     # Annars fortsätter spelet
#     result = "continue"
#     return render_template("new_game.html", word=word, result=result)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seedData()
    app.run(debug=True)

