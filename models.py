from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CryptoProject(db.Model):
    __tablename__ = 'crypto_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    daily = db.Column(db.Boolean)
    airdrop_status = db.Column(db.String(50))
    description = db.Column(db.Text)
    joining_date = db.Column(db.DateTime)
    spent = db.Column(db.Float)
    cryptorank_link = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    profit = db.Column(db.Float, default=0)

    activities = db.relationship('ProjectActivity', backref='project', lazy=True)

    def __repr__(self):
        return f"<Криптопроект {self.name}>"


class ProjectActivity(db.Model):
    __tablename__ = 'project_activity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('crypto_project.id'), nullable=False)

    def __repr__(self):
        return f"<Активность {self.name}>"