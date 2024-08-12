# AWS Marketplace CSV-based Metering Solution
This optional add-on works with the [AWS Marketplace Serverless SaaS Integration](https://github.com/aws-samples/aws-marketplace-serverless-saas-integration) to give sellers a manual, simple, CSV-based method for publishing custom metering usage to AWS Marketplace. **Do not** use this unless you have a Limited or Public listing for a SaaS product on AWS Marketplace using the Serverless SaaS Integration.

## Intended for
- Sellers with a SaaS product listed with "subscription" (usage-based) or "pay-as-you-go" (contract with consumption) [pricing models](https://docs.aws.amazon.com/marketplace/latest/userguide/saas-pricing-models.html) on AWS Marketplace. This does not work with contract-based pricing or other [product deliver methods](https://docs.aws.amazon.com/marketplace/latest/userguide/product-preparation.html).
- Manual reporting of [metered usage records](https://docs.aws.amazon.com/marketplace/latest/userguide/metering-for-usage.html) to AWS Marketplace.
- Sellers with low volume of Marketplace transactions.
- Sellers who need a simple method for reporting metered usage records to AWS Marketplace without involving developers to build a custom integration between their system and AWS.
- Sellers who have a less-technical Seller Admin who need to report metered records to AWS Marketplace on a recurring basis.

## How it works
1. **Manual upload**: Seller (alliance lead) uploads a custom CSV with usage data from their SaaS application, for a specific customer ID gathered from the Subscribers DynamoDB table, to report metered usage for all dimensions and values listed in the CSV to AWS Marketplace.
2. **Event Notification**: A S3 Event Notification triggers a Lambda function automatically once the file is uploaded.
3. **Transform CSV to JSON**: The Lambda function reads the CSV file from the S3 bucket and processes each row of dimensions and values, plus the current timestamp, to created JSON inserting into the Metering Records DynamoDB table.
4. **Insert Item**: The Lambda function inserts the JSON containing the customer ID, all metered dimensions and values, and timestamp to DynamoDB.
5. **Hourly records publish**: Each hour, the Serverless SaaS Integration automatically processes any new records in DynamoDB and publishes them to the the Marketplace API, reflecting state and status back to DynamoDB.

![architecture.png](architecture.png)

## How to deploy the solution
To deploy the AWS Marketplace CSV-based Metering Solution, you'll want to access you AWS seller account as an administrator. Then follow these steps:
1. Obtain the Metering Records table name deployed by the [AWS Marketplace Serverless SaaS Integration](https://github.com/aws-samples/aws-marketplace-serverless-saas-integration) to your account (default is **AWSMarketplaceMeteringRecord**).
2. Using CloudFormation, create a new Stack using the **marketplace-csv-metering.yaml** template in this repo. Input the Subscriber table name into the **DynamoDBMeteringTableName**.
3. After the Stack is created successfully, navigate to the **Resources** tab and open the link to **S3Bucket**.
4. Under **Properties**, navigate to **Event notifications** and click **Create event notification**.
5. Create an event notification with the following:
5.1 Event name: **S3EventNotication**.
5.2 Event types: **Put** / s3:ObjectCreated:Put (only).
5.3 At the bottom, choose the Lambda function created by the Stack: **marketplace-csv-metering-<UI>**.
5.4 Click **Save changes**.
7. use IAM to configure the Role used by your Seller Admin user to have the following permissions:
8. AmazonDynamoDBReadOnly


## Manual CSV Metering
1. Obtain DynamoDB Metering Records table name
2. Deploy marketplace-csv
3. S3 Bucket: add Event Notification trigger for Lambda (s3:ObjectCreated:Put)
4. Create IAM Role for Alliance Lead: RO access to both DynamoDB tables, S3 bucket
5. Obtain CustomerIdentifier from Subscribers table
6. Obtain Usage Dimensions from Marketplace Management Portal
7. Create CSV file: put CustomerIdentifer as name of file (i.e., QEFN33TJED.csv where CustomerIdentifier = QEFN33TJED)
8. In Excel or Text Editor, insert rows for each Usage Dimension and the value to report to Marketplace
9. Save the file, login to AWS and upload to S3 bucket
10. In a few minutes, verify Metereing Records table for new entry
11. In an hour, the entry will update and publish to Marketplace
12. In a day, the CSV file will automatically delete from the S3 bucket
