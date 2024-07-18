from flask import Flask, render_template
from models import db

def create_app():
    flask_app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')


    return flask_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
