import boto3
import json
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    try:
        # Table name
        table_name = "LocIT"
        
        # Scan the table to retrieve all items
        response = dynamodb.scan(TableName=table_name)
        items = response.get('Items', [])
        
        # Format the data into a readable structure
        formatted_data = []
        for item in items:
            formatted_item = {
                "timestamp": item['timestamp']['S'] if 'timestamp' in item else "N/A",
                "latitude": float(item['latitude']['N']) if 'latitude' in item else None,
                "longitude": float(item['longitude']['N']) if 'longitude' in item else None,
                "altitude_ft": int(item['altitude_ft']['N']) if 'altitude_ft' in item else None,
                "speed_mph": int(item['speed_mph']['N']) if 'speed_mph' in item else None,
                "low_battery_mode": item.get('low_battery_mode', {}).get('S', "N/A"),
                "overheat_mode": item.get('overheat_mode', {}).get('S', "N/A"),
                "percent": float(item['percent']['N']) if 'percent' in item else None,
                "temperature_F": float(item['temperature_F']['N']) if 'temperature_F' in item else None,
                "voltage": float(item['voltage']['N']) if 'voltage' in item else None,
            }
            formatted_data.append(formatted_item)
        
        # Filter out invalid timestamps and sort by timestamp in descending order
        valid_data = [
            item for item in formatted_data 
            if item['timestamp'] != "N/A"
        ]
        sorted_data = sorted(
            valid_data, 
            key=lambda x: datetime.strptime(x['timestamp'], "%m/%d/%Y %H:%M:%S"), 
            reverse=True
        )
        
        # Return the sorted data
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(sorted_data, indent=4)  # Pretty-print the JSON
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
