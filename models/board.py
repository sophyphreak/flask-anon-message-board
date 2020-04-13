from db import db


class BoardModel(db.Model):
    __tablename__ = "board"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    threads = db.relationship("ThreadModel")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
