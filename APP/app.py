from flask import Flask, request, render_template
import redis
import os
import pymongo

app = Flask(__name__)

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_connection = redis.from_url(redis_url)

mongo_url = os.getenv("MONGO_URL", "mongodb://root:root@localhost:27017")
mongo_client = pymongo.MongoClient(mongo_url)
mongo_db = mongo_client["visits"]
mongo_collection = mongo_db["ipVisits"]

@app.route("/")
def hello():
    total_visits = redis_connection.incr("count")
    agent = request.headers.get("User-Agent")
    ip = request.remote_addr
    if mongo_collection.count_documents({'address':ip}):
        mongo_collection.update({'address':ip}, {'$inc':{'visits':1}})
    else:
        mongo_collection.insert_one({'address':ip, 'visits':1})
    return render_template("index.html", total_visits=total_visits, agent=agent, ip=ip)

@app.route("/health")
def health():
    return ""

if __name__ == "__main__":
    print("Hello world web app")
    app.run(port=8080, host="0.0.0.0")
