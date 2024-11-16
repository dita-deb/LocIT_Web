from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import boto3
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

# This function will periodically fetch and emit data to clients
def fetch_and_emit_data():
    while True:
        # Fetch data from DynamoDB
        table_name = 'LocIT'
        response = dynamodb.scan(TableName=table_name)

        # Process the data
        formatted_data = []
        for item in response['Items']:
            formatted_item = {
                'ts': item.get('ts', {}).get('N', 'N/A'),
                'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
                'longitude': item.get('longitude', {}).get('N', 'N/A'),
                'latitude': item.get('latitude', {}).get('N', 'N/A'),
                'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
                'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
                'timestamp': item.get('timestamp', {}).get('S', 'N/A')
            }
            formatted_data.append(formatted_item)

        # Emit data to all connected clients via Socket.IO
        socketio.emit('update_data', formatted_data)

        # Wait before fetching data again (set the interval)
        time.sleep(5)  # Update every 5 seconds

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/api/dynamodb', methods=['GET'])
def get_dynamodb_data():
    # Fetch data from DynamoDB
    table_name = 'LocIT'
    response = dynamodb.scan(TableName=table_name)

    # Process the data
    formatted_data = []
    for item in response['Items']:
        formatted_item = {
            'ts': item.get('ts', {}).get('N', 'N/A'),
            'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
            'longitude': item.get('longitude', {}).get('N', 'N/A'),
            'latitude': item.get('latitude', {}).get('N', 'N/A'),
            'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
            'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
            'timestamp': item.get('timestamp', {}).get('S', 'N/A')
        }
        formatted_data.append(formatted_item)

    return jsonify({'data': formatted_data}), 200

# Start the background task
def start_background_task():
    thread = Thread(target=fetch_and_emit_data)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_background_task()  # Start the background task to fetch and emit data
    socketio.run(app, host='0.0.0.0', port=5000)  # Start the Flask server with Socket.IO
