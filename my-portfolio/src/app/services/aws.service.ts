import { Injectable } from '@angular/core';
import * as AWS from 'aws-sdk';
import * as dotenv from 'dotenv';

// Load sensitive data from .env
dotenv.config();

// Import non-sensitive environment variables (like region)
import { environment } from 'C:\Users\mc2di\LocitWeb\LocIT_Web\my-portfolio\src\environments';

@Injectable({
  providedIn: 'root'
})
export class AwsService {
  private dynamoDB: AWS.DynamoDB;

  constructor() {
    // Access environment variables using index signature
    const accessKeyId = process.env['AWS_ACCESS_KEY_ID'];
    const secretAccessKey = process.env['AWS_SECRET_ACCESS_KEY'];

    // Check if the credentials are available, throw an error if not
    if (!accessKeyId || !secretAccessKey) {
      throw new Error('AWS credentials are missing!');
    }

    // Initialize AWS SDK with sensitive data from .env and region from environment.ts
    AWS.config.update({
      region: environment.awsRegion,  // Use region from environment.ts
      credentials: new AWS.Credentials({
        accessKeyId,  // Use sensitive key from .env
        secretAccessKey  // Use sensitive key from .env
      })
    });

    this.dynamoDB = new AWS.DynamoDB();
  }

  // Sample method to get data from DynamoDB
  async getData(params: AWS.DynamoDB.ScanInput) {
    return this.dynamoDB.scan(params).promise();
  }
}
