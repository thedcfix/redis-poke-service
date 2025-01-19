from flask import Flask, render_template_string, jsonify
import redis
import json
import datetime
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize the Flask application
app = Flask(__name__)

# Configure Redis client using environment variables
redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    username=os.getenv('REDIS_USER', 'default'),
    password=os.getenv('REDIS_PASSWORD', None),
    db=int(os.getenv('REDIS_DB', 0))
)

# Configure logging to display time, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def poke_task():
    """
    Task to poke the Redis cache every 12 hours.
    It checks if the 'poke' key exists. If not, it sets the key with the current timestamp.
    """
    try:
        document = redis_client.get('poke')
        if document is not None:
            logging.info("Successfully read 'poke' from Redis.")
        else:
            # Create a JSON document with the current timestamp
            document = json.dumps({'timestamp': datetime.datetime.now().isoformat()})
            redis_client.set('poke', document)
            logging.info("Set new 'poke' document in Redis.")
    except redis.exceptions.RedisError as e:
        logging.error(f"Redis error in poke_task: {e}")

# Initialize and start the background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(poke_task, 'interval', hours=12)
scheduler.start()

# Embedded HTML template using Tailwind CSS for styling
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redis Poke Service</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
        <h1 class="text-3xl font-bold text-gray-800 mb-4 text-center">Redis Poke Service</h1>
        <p class="text-gray-600 text-center">Last successful poke occurred at:</p>
        <p class="text-green-500 font-medium text-center mt-2">{{ last_poked }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """
    Home route that displays the last successful poke timestamp.
    Retrieves the 'poke' key from Redis and passes the timestamp to the HTML template.
    """
    try:
        document = redis_client.get('poke')
        if document:
            data = json.loads(document)
            last_poked = data.get('timestamp', 'Not available')
            logging.info("Successfully retrieved 'poke' timestamp from Redis.")
        else:
            last_poked = 'Never poked.'
            logging.info("No 'poke' timestamp found in Redis.")
    except redis.exceptions.RedisError as e:
        logging.error(f"Redis error while retrieving 'poke': {e}")
        last_poked = 'Error retrieving data.'
    
    return render_template_string(INDEX_HTML, last_poked=last_poked)

@app.route('/healthcheck')
def healthcheck():
    """
    Healthcheck route to verify the Redis connection.
    Returns a JSON response indicating the status.
    """
    try:
        redis_client.ping()
        logging.info("Redis connection successful.")
        return jsonify(status="OK"), 200
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
        return jsonify(status="Redis connection error"), 500

if __name__ == '__main__':
    logging.info("Starting Flask application.")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler shut down successfully.")