from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class stockData(db.Model):
    id = db.Column(db.Integer, primaryKey = True)
    ticker = db.Column(db.String(10), nullable = False)
    date = db.Column(db.Date, nullable = False)
    low = db.Column(db.Float, nullable = False)
    high = db.Column(db.Float, nullable = False)
    open = db.Column(db.Float, nullable = False)
    close = db.Column(db.Float, nullable = False)
    volume = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"{self.ticker} - {self.date} - close: {self.close}" 