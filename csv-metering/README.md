# AWS Marketplace CSV-based Metering Solution
This optional add-on is designed to work with the AWS Marketplace Serverless SaaS Integration to give sellers a manual, simple, CSV-based method for publishing custom metering usage to AWS Marketplace. Do not use this until you have a Public listing for a SaaS product on AWS Marketplace using with the Serverless SaaS Integration deployed.

## Designed for
- Sellers with either SaaS pricing option known as "subscription" (usage-based) or "pay-as-you-go" (contract with consumption). It does *not* work with contract-based pricing.
- Custom, manual reporting of metered usage records to AWS Marketplace.
- Sellers with low volume of Marketplace transactions.
- Sellers who need a manual, simple method for reporting metered usage records without involving developers to build a custom integration between their system and AWS.

## How it works
- Seller gathers usage data from their SaaS application to determine any subscription or pay-as-you-go consumption (beyond contract) metering that needs to be reported to AWS Marketplace to properly bill customers.
- Seller obtains customer identifiers from their Subscribers DynamoDB table.
- Seller creates a custom CSV file for each unique customer identifier, listing each product usage dimension and metering amount.
- Seller uploads each CSV to a S3 bucket. The bucket triggers a Lambda function which transforms and writes the data to the Metering Records DynamoDB table.
- Every hour, any pending records in the Metering Records table are published to the AWS Marketplace BatchMeterUsage API.
- One day later, the CSV file is deleted from the S3 bucket.

## Manual CSV Metering
1. Obtain DynamoDB Metering Records table name
2. Deploy CFT
3. S3 Bucket: add Event Notification trigger for Lambda (s3:ObjectCreated:Put)
