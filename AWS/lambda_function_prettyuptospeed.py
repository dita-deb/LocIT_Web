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
        print(f"Scan response: {json.dumps(response['Items'], indent=4)}")

        # Process the response to clean up and format data
        formatted_data = []
        for item in response['Items']:
            formatted_item = {}
            # Attempt to retrieve the fields with error handling if they don't exist
            try:
                formatted_item['timestamp'] = item['timestamp']['S']
            except KeyError:
                formatted_item['timestamp'] = 'N/A'  # Handle missing 'timestamp'
            
            try:
                formatted_item['latitude'] = float(item['latitude']['N'])
            except KeyError:
                formatted_item['latitude'] = None  # Handle missing 'latitude'

            try:
                formatted_item['longitude'] = float(item['longitude']['N'])
            except KeyError:
                formatted_item['longitude'] = None  # Handle missing 'longitude'

            try:
                formatted_item['altitude_ft'] = int(item['altitude_ft']['N'])
            except KeyError:
                formatted_item['altitude_ft'] = None  # Handle missing 'altitude_ft'

            try:
                formatted_item['speed_mph'] = int(item['speed_mph']['N'])
            except KeyError:
                formatted_item['speed_mph'] = None  # Handle missing 'speed_mph'

            formatted_data.append(formatted_item)

        # Return the formatted data
        return {
            'statusCode': 200,
            'body': json.dumps(formatted_data, indent=4)  # Pretty-printing the JSON response
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
