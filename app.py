from flask import Flask, render_template, request, redirect, url_for
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, CryptoProject, ProjectActivity
from datetime import datetime

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

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
            daily = 1 if daily=='Да' else '0'
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

    @app.route('/project/<string:project_name>')
    def project_detail(project_name):
        project = CryptoProject.query.filter_by(name=project_name).first_or_404()
        activities = ProjectActivity.query.filter_by(project_id=project.id).all()
        return render_template('project_detail.html', project=project, activities=activities)

    return app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True)