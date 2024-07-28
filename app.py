from flask import Flask, render_template, request, redirect, url_for, flash
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, CryptoProject, ProjectLinks, MoneyWay, Thoughts
from flask_migrate import Migrate
from datetime import datetime
import secrets

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        projects = CryptoProject.query.all()
        return render_template('index.html', projects=projects)

    @app.route('/add', methods=['GET', 'POST'])
    def add_project():
        if request.method == 'POST':
            name = request.form['name']
            type_ = request.form['type']
            daily = request.form['daily']
            daily = 1 if daily=='Да' else 0
            airdrop_status = request.form.get('airdrop_status')
            description = request.form.get('description')
            joining_date = request.form.get('joining_date')
            spent = request.form.get('spent')
            cryptorank_link = request.form.get('cryptorank_link')

            # Преобразуем строку даты в объект datetime
            joining_date = datetime.strptime(joining_date, '%Y-%m-%d') if joining_date else None

            # Создаем новый объект CryptoDrop
            new_project = CryptoProject(
                name=name,
                type=type_,
                daily=daily,
                airdrop_status=airdrop_status,
                description=description,
                joining_date=joining_date,
                spent=float(spent),
                cryptorank_link=cryptorank_link
            )

            db.session.add(new_project)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('add_project.html')

    @app.route('/project/<string:project_name>', methods=['GET', 'POST'])
    def project_detail(project_name):
        project = CryptoProject.query.filter_by(name=project_name).first_or_404()
        if request.method == 'POST':
            activity_name = request.form['name']
            activity_link = request.form['link']

            new_activity = ProjectLinks(
                project_id = project.id,
                name = activity_name,
                link = activity_link
            )

            db.session.add(new_activity)
            db.session.commit()
            flash('Активность успешно добавлена', 'success')
            return redirect(url_for('project_detail', project_name=project_name))

        activities = ProjectLinks.query.filter_by(project_id=project.id).all()
        moneyways = MoneyWay.query.filter_by(project_id=project.id).all()
        return render_template('project_detail.html', project=project, activities=activities, moneyways=moneyways)

    @app.route('/edit_project/<string:project_name>', methods=['GET', 'POST'])
    def edit_project(project_name):
        project = CryptoProject.query.filter_by(name=project_name).first_or_404()

        if request.method == 'POST':
            project.name = request.form['name']
            project.type = request.form['type']
            project.daily = int(request.form.get('daily'))
            project.airdrop_status = request.form.get('airdrop_status')
            project.description = request.form.get('description')
            project.joining_date = datetime.strptime(request.form.get('joining_date'), '%d.%m.%Y') if request.form.get(
                'joining_date') else None
            project.cryptorank_link = request.form.get('cryptorank_link')
            project.is_active = 'is_active' in request.form

            db.session.commit()
            flash('Изменения сохранены', 'success')
            return redirect(url_for('project_detail', project_name=project.name))

        return render_template('edit_project.html', project=project)

    return app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True)