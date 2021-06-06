from app import db

class Jokes(db.Model):
    idJoke = db.Column(db.Integer, primary_key=True)
    contentJoke = db.Column(db.String(1024))
    userName = db.Column(db.String(64), db.ForeignKey('user.userName'))
    def __repr__(self):
        return '{s}'.format(s=self.contentJoke)

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(64), index = True, unique = True)
    userPassword = db.Column(db.String(256))
    userJokes = db.relationship('Jokes', backref = 'author', lazy = 'dynamic')
    def __repr__(self):
        return '{s}'.format(s=self.userName)
