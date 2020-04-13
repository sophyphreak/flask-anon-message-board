from db import db
import datetime


class ThreadModel(db.Model):
    __tablename__ = "thread"
    _id = db.Column(db.Integer, primary_key=True)
    board_name = db.Column(db.String(80), db.ForeignKey("board.name"))
    text = db.Column(db.String(80))
    created_on = db.Column(db.DateTime)
    bumped_on = db.Column(db.DateTime)
    reported = db.Column(db.Boolean)
    delete_password = db.Column(db.String(80))
    replies = db.relationship('ReplyModel')

    def __init__(self, board_name, text, delete_password):
        self.board_name = board_name
        self.text = text
        self.created_on = datetime.datetime.utcnow()
        self.bumped_on = datetime.datetime.utcnow()
        self.reported = False
        self.delete_password = delete_password

    def json(self):
        return {
            "_id": self._id,
            "board_name": self.board_name,
            "text": self.text,
            "created_on": self.created_on.isoformat(),
            "bumped_on": self.bumped_on.isoformat(),
            "replies": self.get_replies_list()
        }

    def get_replies_list(self):
        if self.replies:
            replies = sorted(self.replies, reverse=True, key=lambda reply: reply.created_on)
            return [reply.json() for reply in replies]
        else:
            return []


    @classmethod
    def find_by_board_name(cls, board_name):
        return cls.query.filter_by(board_name=board_name).order_by(ThreadModel.bumped_on.desc()).limit(10).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
