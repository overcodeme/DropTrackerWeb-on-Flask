from flask import Flask, render_template, request, redirect, url_for
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, CryptoDrop
from datetime import datetime

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add', methods=['GET', 'POST'])
    def add_project():
        if request.method == 'POST':
            name = request.form['name']
            type_ = request.form['type']
            daily = 'daily' in request.form
            airdrop_status = request.form.get('airdrop_status')
            description = request.form.get('description')
            fundraising = request.form.get('fundraising')
            joining_date = request.form.get('joining_date')
            spent = request.form.get('spent')
            cryptorank_link = request.form.get('cryptorank_link')

            # Преобразуем строку даты в объект datetime
            joining_date = datetime.strptime(joining_date, '%Y-%m-%d') if joining_date else None

            # Создаем новый объект CryptoDrop
            new_project = CryptoDrop(
                name=name,
                type=type_,
                daily=daily,
                airdrop_status=airdrop_status,
                description=description,
                fundraising=float(fundraising) if fundraising else None,
                joining_date=joining_date,
                spent=float(spent) if spent else None,
                cryptorank_link=cryptorank_link
            )

            db.session.add(new_project)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('add_project.html')

    return app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True)