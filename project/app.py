import os

from flask import Flask
from redis import Redis

app = Flask(__name__)

redis = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
)


@app.route("/")
def hello():
    count = redis.incr("hits")
    return f"Hello from Docker! I have been seen {count} time(s).\n"
