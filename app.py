import os
from flask import Flask, render_template
from seed import seedData
from database import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from forms import GuessForm

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
db.init_app(app)
migrate= Migrate(app, db)

# render to main page

@app.route('/')
def index():
    return render_template('index.html')


#guess

@app.route("/", methods=["GET", "POST"])
def index():
    form = GuessForm()

    if form.validate_on_submit():
        guess = form.guess.data.lower()
        print("User guess:", guess)  # later: compare with the secret word

    return render_template("index.html", form=form)
if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        seedData()