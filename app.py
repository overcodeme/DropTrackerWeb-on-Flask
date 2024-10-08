from flask import Flask, render_template, request, redirect, url_for, flash
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, CryptoProject, ProjectLinks
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
        filter_type = request.args.get('filter', 'Все')
        search_query = request.args.get('search', '')

        print(filter_type)
        print(search_query)

        projects = CryptoProject.query

        if filter_type == 'active':
            projects = projects.filter_by(is_active=True)
        elif filter_type == 'daily':
            projects = projects.filter_by(daily=True)
        elif filter_type == 'social':
            projects = projects.filter_by(type='Социалки')
        elif filter_type == 'testnets':
            projects = projects.filter_by(type='Тестнет')
        elif filter_type == 'completed':
            projects = projects.filter_by(is_active=False)

        if search_query:
            projects = projects.filter(CryptoProject.name.ilike(f'%{search_query}%'))

        projects = projects.all()

        return render_template('index.html', projects=projects)

    @app.route('/add', methods=['GET', 'POST'])
    def add_project():
        if request.method == 'POST':
            name = request.form['name']
            type_ = request.form['type']
            fundraising = request.form['fundraising']
            daily = request.form['daily']
            daily = 1 if daily=='Да' else 0
            airdrop_status = request.form['airdrop_status']
            description = request.form['description']
            joining_date = request.form['joining_date']
            cryptorank_link = request.form['cryptorank_link']

            joining_date = datetime.strptime(joining_date, '%Y-%m-%d') if joining_date else None

            new_project = CryptoProject(
                name=name,
                type=type_,
                daily=daily,
                airdrop_status=airdrop_status,
                description=description,
                joining_date=joining_date,
                cryptorank_link=cryptorank_link,
                fundraising=fundraising
            )

            db.session.add(new_project)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('add_project.html')

    @app.route('/project/<string:project_name>', methods=['GET', 'POST'])
    def project_detail(project_name):
        project = CryptoProject.query.filter_by(name=project_name).first_or_404()
        links = ProjectLinks.query.filter_by(project_id=project.id).all()

        if request.method == 'POST':
            activity_name = request.form['activity_name']
            activity_link = request.form['activity_link']
            creating_date = datetime.now().strftime('%d.%m.%Y')

            new_link = ProjectLinks(
                activity_name=activity_name,
                activity_link=activity_link,
                creating_date=creating_date,
                project_id=project.id
            )

            db.session.add(new_link)
            db.session.commit()

            return redirect(url_for('project_detail', project_name=project.name))

        print(links)
        return render_template('project_detail.html', project=project, links=links)

    @app.route('/edit_project/<string:project_name>', methods=['GET', 'POST'])
    def edit_project(project_name):
        project = CryptoProject.query.filter_by(name=project_name).first_or_404()

        if request.method == 'POST':
            project.name = request.form['name']
            project.type = request.form['type']
            project.fundraising = request.form['fundraising']
            project.daily = int(request.form.get('daily'))
            project.airdrop_status = request.form.get('airdrop_status')
            project.description = request.form.get('description')
            project.joining_date = datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d') if request.form.get(
                'joining_date') else None
            project.cryptorank_link = request.form.get('cryptorank_link')
            project.is_active = 'is_active' in request.form

            db.session.commit()
            flash('Изменения сохранены', 'success')
            return redirect(url_for('project_detail', project_name=project.name))

        return render_template('edit_project.html', project=project)

    @app.route('/delete_project/<int:project_id>', methods=['POST'])
    def delete_project(project_id):
        project = CryptoProject.query.get(project_id)
        print(project)
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('index'))


    @app.route('/delete_activity/<int:activity_id>', methods=['POST'])
    def delete_activity(activity_id):
        activity = ProjectLinks.query.get(activity_id)
        db.session.delete(activity)
        db.session.commit()
        return redirect(url_for('index'))


    return app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True)