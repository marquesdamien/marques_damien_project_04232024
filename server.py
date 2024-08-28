from flask_app import app

from flask_app.controllers import cards, users, decks

if __name__ == "__main__":
    app.run(debug=True)