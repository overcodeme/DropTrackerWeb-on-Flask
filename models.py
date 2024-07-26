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
    cryptorank_link = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    profit = db.Column(db.Float, default=0)

    activities = db.relationship('ProjectLinks', backref='project', lazy=True)
    spent = db.relationship('MoneyWay', backref='project', lazy=True)
    thoughts = db.relationship('Thoughts', backref='project', lazy=True)

    def __repr__(self):
        return f"<Криптопроект {self.name}>"


class ProjectLinks(db.Model):
    __tablename__ = 'project_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('crypto_project.id'), nullable=False)


class MoneyWay(db.Model):
    __tablename__ = 'project_invest'
    id = db.Column(db.Integer, primary_key=True)
    invest_detail = db.Column(db.String(100))
    invest_amount = db.Column(db.Float)
    profit_detail = db.Column(db.String(100))
    profit_amount = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('crypto_project.id'), nullable=False)


class Thoughts(db.Model):
    __tablename__ = 'thoughts'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    project_id =  db.Column(db.Integer, db.ForeignKey('crypto_project.id'), nullable=False)