# Tested with Python 3.7
import json
import boto3
import csv
import time


def lambda_handler(event, context):

    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        tmp_path = '/tmp/' + key

        # print(bucket)
        # print(key)

        s3.download_file(bucket, key, tmp_path)

        dimension_usage = []

        with open(tmp_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0

            for row in csv_reader:
                if row_count != 0:
                    # print(row)
                    dimension_usage_map = {
                        "M": {
                            "dimension": {
                                "S": row[0]
                            },
                            "value": {
                                "S": row[1]
                            }
                        }
                    }
                    dimension_usage.append(dimension_usage_map)
                row_count += 1

        # print(dimension_usage)

        epoch_time = round(time.time())
        # print(epoch_time)

        dynamodb_item = {
            "create_timestamp": {
                "N": str(epoch_time)
            },
            "customerIdentifier": {
                "S": key[:-4]
            },
            "dimension_usage": {
                "L": dimension_usage
            },
            "metering_pending": {
                "S": "true"
            }
        }

        # print(json.dumps(dynamodb_item))

        dynamodb.put_item(
            TableName='AWSMarketplaceMeteringRecords',
            Item=dynamodb_item
        )
    return {
        'statusCode': 200,
        'body': json.dumps(dynamodb_item)
    }
