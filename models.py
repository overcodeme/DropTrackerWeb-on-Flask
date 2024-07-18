from sqlalchemy import SQLALchemy

db = SQLALchemy()

class CryptoDrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100))
    description = db.Column(db.Text)
    fundraising = db.Column(db.Float)
    joining_date = db.Column(db.DateTime)
    spend = db.Column(db.Float)
    cryptorank_link = db.Column(db.String(200))

    def __repr__(self):
        return f"<Crypto project {self.name}>"