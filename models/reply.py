from db import db
import datetime


class ReplyModel(db.Model):
    __tablename__ = "reply"
    _id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    created_on = db.Column(db.DateTime)
    reported = db.Column(db.Boolean)
    delete_password = db.Column(db.String(80))
    thread_id = db.Column(db.Integer, db.ForeignKey("thread._id"))

    def __init__(self, text, delete_password, thread_id):
        self.text = text
        self.created_on = datetime.datetime.utcnow()
        self.reported = False
        self.delete_password = delete_password
        self.thread_id = thread_id

    def json(self):
        return {
            "_id": self._id,
            "text": self.text,
            "created_on": self.created_on.isoformat(),
            "thread_id": self.thread_id,
        }

    @classmethod
    def find_by_thread_id(cls, thread_id):
        return cls.query.filter_by(thread_id=thread_id).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
