# AWS Marketplace CSV-based Metering Solution
This optional add-on is designed to work with the [AWS Marketplace Serverless SaaS Integration](https://github.com/aws-samples/aws-marketplace-serverless-saas-integration) to give sellers a manual, simple, CSV-based method for publishing custom metering usage to AWS Marketplace. **Do not** use this unless you have a Limited or Public listing for a SaaS product on AWS Marketplace using the Serverless SaaS Integration.

## Intended for
- Sellers with a SaaS product, with pricing option "subscription" (usage-based) or "pay-as-you-go" (contract with consumption). This does not work with contract-based pricing.
- Manual reporting of metered usage records to AWS Marketplace.
- Sellers with low volume of Marketplace transactions.
- Sellers who need a simple method for reporting metered usage records to AWS Marketplace without involving developers to build a custom integration between their system and AWS.

## How it works
1. **Manual upload**: Seller (alliance lead) uploads a custom CSV with usage data from their SaaS application, for a specific customer ID gathered from the Subscribers DynamoDB table, to report metered usage for all dimensions and values listed in the CSV to AWS Marketplace.
2. **Event Notification**: A S3 Event Notification triggers a Lambda function automatically once the file is uploaded.
3. **Transform CSV to JSON**: The Lambda function reads the CSV file from the S3 bucket and processes each row of dimensions and values, plus the current timestamp, to created JSON inserting into the Metering Records DynamoDB table.
4. **Insert Item**: The Lambda function inserts the JSON containing the customer ID, all metered dimensions and values, and timestamp to DynamoDB.
5. **Hourly records publish**: Each hour, the Serverless SaaS Integration automatically processes any new records in DynamoDB and publishes them to the the Marketplace API, reflecting state and status back to DynamoDB.

![architecture.png](architecture.png)

## Manual CSV Metering
1. Obtain DynamoDB Metering Records table name
2. Deploy CFT
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
