from flask import Flask
from flask_restful import Api
from db import db
import os

from resources.reply import Reply
from resources.thread import Thread

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///anon-message-board"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Reply, "/api/replies/<board>")
api.add_resource(Thread, "/api/threads/<board>")

if __name__ == "__main__":
    app.run(debug=True)
