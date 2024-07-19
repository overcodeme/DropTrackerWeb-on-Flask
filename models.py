from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CryptoDrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    daily = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(100))
    description = db.Column(db.Text)
    fundraising = db.Column(db.Float)
    joining_date = db.Column(db.DateTime)
    spent = db.Column(db.Float)
    cryptorank_link = db.Column(db.String(200))

    def __repr__(self):
        return f"<Crypto project {self.name}>"