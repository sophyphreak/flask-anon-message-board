from flask_restful import Resource, reqparse
import datetime

from models.reply import ReplyModel
from models.thread import ThreadModel


class Reply(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("text", type=str)
    parser.add_argument(
        "delete_password", type=str,
    )
    parser.add_argument("thread_id", type=str)
    parser.add_argument("reply_id", type=str)

    def post(self, board_name):
        data = Reply.parser.parse_args()
        text = data["text"]
        delete_password = data["delete_password"]
        thread_id = data["thread_id"]

        new_reply = ReplyModel(
            text=text, delete_password=delete_password, thread_id=thread_id
        )
        new_reply.save_to_db()
        return new_reply.json(), 201

    def get(self, board_name):
        thread_id = Reply.parser.parse_args()["thread_id"]
        thread = ThreadModel.find_by_id(_id=thread_id)
        return thread.json()

    def delete(self, board_name):
        data = Reply.parser.parse_args()
        thread_id = data["thread_id"]
        delete_password = data["delete_password"]
        reply_id = data["reply_id"]
        reply = ReplyModel.find_by_id(_id=reply_id)
        if reply.delete_password == delete_password:
            reply.text = "[deleted]"
            reply.save_to_db()
            return {"message": "success"}
        return {"message": "incorrect password"}

    def put(self, board_name):
        reply_id = Reply.parser.parse_args()["reply_id"]
        reply = ReplyModel.find_by_id(_id=reply_id)
        reply.reported = True
        reply.save_to_db()
        return {"message": "success"}
