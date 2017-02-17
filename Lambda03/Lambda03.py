from __future__ import print_function

import boto3
import json

print('Loading function')
s3 = boto3.resource('s3')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''takes a query String parameter 'bucket' that maps to a bucketname
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operation = event['httpMethod']
    
    payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
    print(payload)
    bucket = s3.Bucket(payload["bucket"])
    news = []
    for obj in bucket.objects.all():
      news.append({'title':'','url':"https://s3.amazonaws.com/"+payload['bucket']+"/"+obj.key})
      print(obj.key)

    return respond(None, news)
    
