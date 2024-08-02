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
    thoughts = db.Column(db.String)
    joining_date = db.Column(db.DateTime)
    cryptorank_link = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    profit = db.Column(db.Float, default=0)

    project_links = db.relationship('ProjectLinks', backref='project', lazy=True)

    def __repr__(self):
        return f"<Криптопроект {self.name}>"


class ProjectLinks(db.Model):
    __tablename__ = 'project_links'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(100))
    activity_link = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('crypto_project.id'), nullable=False)
    creating_date = db.Column(db.String)

    def __repr__(self):
        return f"{self.activity_name}"
