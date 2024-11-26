# from flask import Flask, jsonify, render_template
# from flask_socketio import SocketIO, emit
# import boto3
# import time
# from threading import Thread

# app = Flask(__name__)
# socketio = SocketIO(app)

# # Initialize DynamoDB client
# dynamodb = boto3.client('dynamodb', region_name='us-east-2')

# # This function will periodically fetch and emit data to clients
# def fetch_and_emit_data():
#     while True:
#         # Fetch data from DynamoDB
#         table_name = 'LocIT'
#         response = dynamodb.scan(TableName=table_name)

#         # Process the data
#         formatted_data = []
#         for item in response['Items']:
#             formatted_item = {
#                 'ts': item.get('ts', {}).get('N', 'N/A'),
#                 'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
#                 'longitude': item.get('longitude', {}).get('N', 'N/A'),
#                 'latitude': item.get('latitude', {}).get('N', 'N/A'),
#                 'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
#                 'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
#                 'timestamp': item.get('timestamp', {}).get('S', 'N/A')
#             }
#             formatted_data.append(formatted_item)

#         # Emit data to all connected clients via Socket.IO
#         socketio.emit('update_data', formatted_data)

#         # Wait before fetching data again (set the interval)
#         time.sleep(5)  # Update every 5 seconds

# @app.route('/')
# def index():
#     return render_template('index.html')  # Render the index.html template

# @app.route('/api/dynamodb', methods=['GET'])
# def get_dynamodb_data():
#     # Fetch data from DynamoDB
#     table_name = 'LocIT'
#     response = dynamodb.scan(TableName=table_name)

#     # Process the data
#     formatted_data = []
#     for item in response['Items']:
#         formatted_item = {
#             'ts': item.get('ts', {}).get('N', 'N/A'),
#             'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
#             'longitude': item.get('longitude', {}).get('N', 'N/A'),
#             'latitude': item.get('latitude', {}).get('N', 'N/A'),
#             'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
#             'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
#             'timestamp': item.get('timestamp', {}).get('S', 'N/A')
#         }
#         formatted_data.append(formatted_item)

#     return jsonify({'data': formatted_data}), 200

# # Start the background task
# def start_background_task():
#     thread = Thread(target=fetch_and_emit_data)
#     thread.daemon = True
#     thread.start()

# if __name__ == "__main__":
#     start_background_task()  # Start the background task to fetch and emit data
#     socketio.run(app, host='0.0.0.0', port=5000)  # Start the Flask server with Socket.IO

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import boto3
import time
from threading import Thread
import os

# Load environment variables securely (remove hardcoded AWS credentials)
aws_region = os.getenv('AWS_REGION', 'us-east-2')
aws_access_key_id = os.getenv('AKIAUMYCIA4OK2DVRFOH')
aws_secret_access_key = os.getenv('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')

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize DynamoDB client with environment variables
dynamodb = boto3.client(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Function to fetch and emit data
def fetch_and_emit_data():
    while True:
        try:
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
        except Exception as e:
            print(f"Error fetching data from DynamoDB: {e}")
            time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/api/dynamodb', methods=['GET'])
def get_dynamodb_data():
    try:
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
    except Exception as e:
        print(f"Error fetching data from DynamoDB: {e}")
        return jsonify({'error': 'Failed to retrieve data'}), 500

# Start the background task
def start_background_task():
    thread = Thread(target=fetch_and_emit_data)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_background_task()  # Start the background task to fetch and emit data
    socketio.run(app, host='0.0.0.0', port=5000)  # Start the Flask server with Socket.IO

# from flask import Flask, jsonify, render_template
# from flask_socketio import SocketIO, emit
# import boto3
# import time
# from threading import Thread
# import os

# # Load environment variables

# # Initialize Flask app and SocketIO
# app = Flask(__name__)
# socketio = SocketIO(app)

# # Initialize DynamoDB client with environment variables
# dynamodb = boto3.client(
#     'dynamodb',
#     region_name=os.getenv('AWS_REGION', 'us-east-2'),
#     aws_access_key_id=os.getenv('AKIAUMYCIA4OK2DVRFOH'),
#     aws_secret_access_key=os.getenv('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')
# )

# # Function to fetch and emit data
# def fetch_and_emit_data():
#     while True:
#         try:
#             # Fetch data from DynamoDB
#             table_name = 'LocIT'
#             response = dynamodb.scan(TableName=table_name)

#             # Process the data
#             formatted_data = []
#             for item in response['Items']:
#                 formatted_item = {
#                     'ts': item.get('ts', {}).get('N', 'N/A'),
#                     'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
#                     'longitude': item.get('longitude', {}).get('N', 'N/A'),
#                     'latitude': item.get('latitude', {}).get('N', 'N/A'),
#                     'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
#                     'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
#                     'timestamp': item.get('timestamp', {}).get('S', 'N/A')
#                 }
#                 formatted_data.append(formatted_item)

#             # Emit data to all connected clients via Socket.IO
#             socketio.emit('update_data', formatted_data)

#             # Wait before fetching data again (set the interval)
#             time.sleep(5)  # Update every 5 seconds
#         except Exception as e:
#             print(f"Error fetching data from DynamoDB: {e}")
#             time.sleep(5)

# @app.route('/')
# def index():
#     return render_template('index.html')  # Render the index.html template

# @app.route('/api/dynamodb', methods=['GET'])
# def get_dynamodb_data():
#     try:
#         # Fetch data from DynamoDB
#         table_name = 'LocIT'
#         response = dynamodb.scan(TableName=table_name)

#         # Process the data
#         formatted_data = []
#         for item in response['Items']:
#             formatted_item = {
#                 'ts': item.get('ts', {}).get('N', 'N/A'),
#                 'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
#                 'longitude': item.get('longitude', {}).get('N', 'N/A'),
#                 'latitude': item.get('latitude', {}).get('N', 'N/A'),
#                 'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
#                 'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),
#                 'timestamp': item.get('timestamp', {}).get('S', 'N/A')
#             }
#             formatted_data.append(formatted_item)

#         return jsonify({'data': formatted_data}), 200
#     except Exception as e:
#         print(f"Error fetching data from DynamoDB: {e}")
#         return jsonify({'error': 'Failed to retrieve data'}), 500

# # Start the background task
# def start_background_task():
#     thread = Thread(target=fetch_and_emit_data)
#     thread.daemon = True
#     thread.start()

# if __name__ == "__main__":
#     start_background_task()  # Start the background task to fetch and emit data
#     socketio.run(app, host='0.0.0.0', port=5000)  # Start the Flask server with Socket.IO



# from waitress import serve
# from fetch_dynamodb_data import app

# if __name__ == "__main__":
#     start_background_task()  # Start the background task to fetch and emit data
#     socketio.run(app, host='0.0.0.0', port=5000)  # Start the Flask server with Socket.IO

