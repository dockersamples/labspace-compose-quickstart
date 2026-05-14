import os

from flask import Flask, render_template
from redis import Redis

app = Flask(__name__)

redis = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
)


@app.route("/")
def hello():
    count = redis.incr("hits")
    message = "Your containerized app is running?"
    return render_template("index.html", count=count, message=message)
