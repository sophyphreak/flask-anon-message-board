from flask_restful import Resource, reqparse
import datetime

from models.thread import ThreadModel
from models.board import BoardModel


class Thread(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "text",
        type=str
    )
    parser.add_argument(
        "delete_password",
        type=str,
    )
    parser.add_argument(
        "thread_id",
        type=str
    )

    def post(self, board_name):
        data = Thread.parser.parse_args()
        text = data["text"]
        delete_password = data["delete_password"]

        board = BoardModel.find_by_name(name=board_name)
        if not board:
            new_board = BoardModel(name=board_name)
            new_board.save_to_db()

        new_thread = ThreadModel(board_name=board_name, text=text, delete_password=delete_password)
        new_thread.save_to_db()
        return new_thread.json(), 201
    
    def get(self, board_name):
        threads = ThreadModel.find_by_board_name(board_name=board_name)
        threads_jsons = [thread.json() for thread in threads]
        return [reduce_replies_to_three(thread_json) for thread_json in threads_jsons]

    def delete(self, board_name):
        data = Thread.parser.parse_args()
        delete_password = data['delete_password']
        thread_id = data['thread_id']
        thread = ThreadModel.find_by_id(_id=thread_id)
        if thread.delete_password == delete_password:
            thread.delete_from_db()
            return {"message": "success"}
        return {"message": "incorrect password"}

    def put(self, board_name):
        thread_id = Thread.parser.parse_args()['thread_id']
        thread = ThreadModel.find_by_id(_id=thread_id)
        thread.reported = True
        thread.save_to_db()
        return {"message": "success"}


def reduce_replies_to_three(thread_json):
    thread_json['replies'] = thread_json['replies'][0:3]
    return thread_json

