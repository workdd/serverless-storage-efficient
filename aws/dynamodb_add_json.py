import boto3

table_name = ''
region_name = ''
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)
response = table.put_item(
    Item={
        'inputdata': 'inputdata'
    }
)
