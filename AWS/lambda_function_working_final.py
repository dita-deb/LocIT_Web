import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event:", json.dumps(event))

        # Use the correct table name 'LocIT'
        table_name = "LocIT"
        
        # Perform the Scan operation on the table
        print(f"Scanning table: {table_name}")
        response = dynamodb.scan(TableName=table_name)
        
        # Log the raw items for inspection
        print(f"Scan response: {json.dumps(response)}")

        if 'Items' not in response:
            raise ValueError("No 'Items' found in response")
        
        # Process the response to clean up and format data
        formatted_data = []
        for item in response['Items']:
            formatted_item = {}

            # Process each attribute with error handling

            try:
                formatted_item['timestamp'] = item.get('timestamp', {}).get('S', 'N/A')
            except KeyError:
                formatted_item['timestamp'] = 'N/A'

            try:
                formatted_item['latitude'] = float(item.get('latitude', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['latitude'] = None

            try:
                formatted_item['longitude'] = float(item.get('longitude', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['longitude'] = None

            try:
                formatted_item['altitude_ft'] = int(item.get('altitude_ft', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['altitude_ft'] = None

            try:
                formatted_item['speed_mph'] = int(item.get('speed_mph', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['speed_mph'] = None

            try:
                formatted_item['low_battery_mode'] = item.get('low_battery_mode', {}).get('S', 'N/A')
            except KeyError:
                formatted_item['low_battery_mode'] = 'N/A'

            try:
                formatted_item['overheat_mode'] = item.get('overheat_mode', {}).get('S', 'N/A')
            except KeyError:
                formatted_item['overheat_mode'] = 'N/A'

            try:
                formatted_item['percent'] = int(item.get('percent', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['percent'] = None

            try:
                formatted_item['temperature_F'] = float(item.get('temperature_F', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['temperature_F'] = None

            try:
                formatted_item['voltage'] = float(item.get('voltage', {}).get('N', None))
            except (ValueError, TypeError):
                formatted_item['voltage'] = None

            formatted_data.append(formatted_item)

        # Log formatted data before returning
        print(f"Formatted Data: {json.dumps(formatted_data, indent=4)}")

        # Return the formatted data inside the lambda_handler function
        return {
            'statusCode': 200,
            'body': json.dumps(formatted_data, indent=4)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
