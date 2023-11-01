# Alternate Mechanism - CSV Metering Records Upload

In order to meter for usage using the [AWS Marketplace Serverless SaaS Partner Solution](https://aws.amazon.com/solutions/implementations/aws-marketplace-saas/), the documentation describes updating the [**AWSMarketplaceMeteringRecords** DynamoDB table with a JSON record](https://aws-ia.github.io/cloudformation-aws-marketplace-saas/#_meter_for_usage) for the customer identifier and each dimension + value to be metered.

## Solution

**Note**: this solution is designed to work with the AWS Marketplace Serverless SaaS Partner Solution. The partner must already have this deployed. 

This solution uses the following:

* **CSV file** (s3 / customerIdentifier.csv) - used to capture the dimensions, metered value and customer identifier needed to send to Marketplace.
* **IAM user** - used to grant access to a partner (Alliance Lead) to upload to S3.
* **S3 bucket** - destination for uploading CSV file(s) for each customer, each time they need to meter usage.
* **Lambda function** (lambda / marketplace-csv-to-dynamodb / lambda_function.py) - transforms CSV to JSON, and put as a new item in the AWSMarketplaceMeteringRecords DynamoDB table.

The intent behind this solution is to allow:
* Less technical partner Alliance Leads to submit metering updates to Marketplace without crafting custom JSON.
* Simplify authorization and authentication with a basic S3 upload process.

## How it works

Rather than having partners manually update a DynamoDB table manually with JSON, I've created a simpler CSV-based solution that works as follows:

1. Partner fills out a template CSV file for the specific customer and product dimensions that need to be metered:

**customerIdentifier.csv** - partner replaces the **customerIdentifier** with the exact identifier in Marketplace.

**dimension_1_id,1** - for each row in the CSV, partner replaces **dimension_1_id** with the exact product dimension name and **1** with the value.

2. Partner is logs in to their AWS account using the IAM user with upload access to the target S3 bucket.

3. Partner uploads CSV(s) to the S3 bucket.

4. A S3 Event Notification invokes the Lambda function based on the PutObject event.

5. The Lambda function reads in the CSV file, transforms it to the JSON format required for DynamoDB item entry, then creates the item in the AWSMarketplaceMeteringRecords table.

6. Within an hour, the serverless solution posts the updated items to the Marketplace API.

### Sample CSV

    customerIdentifier.csv

    dimension,value
    dimension_1_id,1
    dimension_2_id,2
    dimension_3_id,3

### Transformed JSON for DynamoDB item creation

    {
        "create_timestamp": {
            "N": "1686938713"
        },
        "customerIdentifier": {
            "S": "customerIdentifier"
        },
        "dimension_usage": {
            "L": [
                {
                    "M": {
                        "dimension": {
                            "S": "dimension_1_id"
                        },
                        "value": {
                            "S": "1"
                        }
                    }
                },
                {
                    "M": {
                        "dimension": {
                            "S": "dimension_2_id"
                        },
                        "value": {
                            "S": "2"
                        }
                    }
                },
                {
                    "M": {
                        "dimension": {
                            "S": "dimension_3_id"
                        },
                        "value": {
                            "S": "3"
                        }
                    }
                }
            ]
        },
        "metering_pending": {
            "S": "true"
        }
    }

## Lambda function permissions

In order to authorize Lambda to read the CSV file from S3 and put an item in the DynamoDB table, you'll need to update the Lambda execution role to include additional permissions (sample - replace <bucket-name> below):

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "logs:CreateLogGroup",
                "Resource": "arn:aws:logs:us-east-1:868121969675:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:us-east-1:868121969675:log-group:/aws/lambda/MarketplaceCSVtoDynamoDB:*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": [
                    "arn:aws:s3:::<bucket-name>/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem"
                ],
                "Resource": [
                    "arn:aws:dynamodb:*:*:table/AWSMarketplaceMeteringRecords"
                ]
            }
        ]
    }