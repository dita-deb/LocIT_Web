from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

# Define the root path
@app.route('/')
def root():
    return "Flask app is running. Access the API at /api/dynamodb"

# Define route to fetch data from DynamoDB
@app.route('/api/dynamodb', methods=['GET'])
def fetch_table_data():
    table_name = 'LocIT'  # Use your table name here
    response = dynamodb.scan(TableName=table_name)
    
    # Optional: Format the data before sending it to the front-end
    formatted_data = []
    for item in response['Items']:
        formatted_item = {
            'ts': item.get('ts', {}).get('N', 'N/A'),  # Default to 'N/A' if not found
            'altitude_ft': item.get('altitude_ft', {}).get('N', 'N/A'),
            'longitude': item.get('longitude', {}).get('N', 'N/A'),
            'latitude': item.get('latitude', {}).get('N', 'N/A'),
            'sensorID': item.get('sensorID', {}).get('S', 'N/A'),
            'speed_mph': item.get('speed_mph', {}).get('N', 'N/A'),  # Handles NULL values
        }
        
        # Handle 'timestamp' which may be missing
        timestamp = item.get('timestamp', {}).get('S', 'N/A')  # Default to 'N/A' if missing
        formatted_item['timestamp'] = timestamp
        
        formatted_data.append(formatted_item)

    return jsonify(formatted_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
