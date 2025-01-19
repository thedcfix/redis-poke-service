from flask import Flask, render_template, jsonify
import redis
import json
import time
import datetime
import os
import logging

app = Flask(__name__)
redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    username=os.getenv('REDIS_USER', 'default'),
    password=os.getenv('REDIS_PASSWORD', None),
    db=int(os.getenv('REDIS_DB', 0))
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/poke')
def poke():
    while True:
        try:
            document = redis_client.get('poke')
            if document is not None:
                logging.info("Successfully read 'poke' from Redis.")
            else:
                document = json.dumps({'timestamp': datetime.datetime.now().isoformat()})
                redis_client.set('poke', document)
                logging.info("Set new 'poke' document in Redis.")
        except redis.exceptions.RedisError as e:
            logging.error(f"Redis error in /poke endpoint: {e}")
        time.sleep(43200)  # Sleep for 12 hours

@app.route('/healthcheck')
def healthcheck():
    try:
        redis_client.ping()
        return jsonify(status="OK"), 200
    except redis.exceptions.ConnectionError:
        return jsonify(status="Redis connection error"), 500

if __name__ == '__main__':
    app.run(debug=True)
