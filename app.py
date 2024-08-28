from flask import Flask, request, render_template, redirect, url_for
import redis

app = Flask(__name__)

# Connect to the Redis cloud instance
# Replace with your cloud Redis credentials
redis_host = 'redis-15726.c92.us-east-1-3.ec2.redns.redis-cloud.com'       # e.g., 'your-redis-instance.xxxxxx.ng.0001.use1.cache.amazonaws.com'
redis_port = 15726                    # Default Redis port
redis_password = 'e02Y34gZ7rwrU2cBDVD1Ugx8mx1tzw33'

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    ssl=False
)


@app.route('/', methods=['GET'])
def index():
    keys = r.keys()
    values = {}
    for key in keys:
        key_type = r.type(key).decode('utf-8')
        if key_type == 'string':
            values[key.decode('utf-8')] = r.get(key).decode('utf-8')
        elif key_type == 'hash':
            values[key.decode('utf-8')] = r.hgetall(key)
        elif key_type == 'list':
            values[key.decode('utf-8')] = r.lrange(key, 0, -1)
    return render_template('index.html', keys=keys, values=values)


@app.route('/insert', methods=['POST'])
def insert_data():
    key = request.form['key']
    value = request.form['value']
    # Insert data into Redis
    r.set(key, value)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
