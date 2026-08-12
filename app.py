from flask import Flask, jsonify
import redis, os

app = Flask(__name__)

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=6379,
    socket_connect_timeout=2
)

@app.route("/")
def visit():
    count = r.incr("visits")           # ask Redis to add 1 and give back the new total
    return jsonify(message="Hello!", total_visits=count)

@app.route("/health")
def health():
    try:
        r.ping()                       # actually check Redis is reachable
        return jsonify(status="ok"), 200
    except redis.exceptions.RedisError:
        return jsonify(status="db unreachable"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)