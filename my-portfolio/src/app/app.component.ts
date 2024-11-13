import { Component, OnInit } from '@angular/core';
import { AwsService } from './services/aws.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  data: any;

  constructor(private awsService: AwsService) {}

  ngOnInit(): void {
    this.fetchDataFromDynamoDB();
  }

  async fetchDataFromDynamoDB() {
    const params = {
      TableName: 'LocIT'  // Replace with your actual DynamoDB table name
    };

    try {
      const result = await this.awsService.getData(params);
      this.data = result.Items;  // Assuming you're working with a list of items
      console.log('DynamoDB Data:', this.data);
    } catch (error) {
      console.error('Error fetching data from DynamoDB:', error);
    }
  }
}
