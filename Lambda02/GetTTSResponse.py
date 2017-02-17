# -*- coding: utf-8 -*-

import boto3
import hashlib
import botocore.exceptions
import json

config = {
    'ru': {'voice': 'Maxim'},
    'fr': {'voice': 'Mathieu'},
    'en': {'voice': 'Joanna'},
    'nl': {'voice': 'Ruben'},
    'sv': {'voice': 'Astrid'},
    'pt': {'voice': 'Ines'},
    'nb': {'voice': 'Liv'},
    'de': {'voice': 'Marlene'},
    'tr': {'voice': 'Filiz'},
    'it': {'voice': 'Giorgio'},
    'da': {'voice': 'Naja'},
    'cy': {'voice': 'Gwyneth'},
    'pl': {'voice': 'Maja'},
    'es': {'voice': 'Penelope'},
    'ro': {'voice': 'Carmen'},
    'ja': {'voice': 'Mizuki'},
    'is': {'voice': 'Karl'}
}

s3 = boto3.resource('s3')

def convert(text, filename, language):
    client = boto3.client('polly')

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId=config.get(language).get('voice')
    )

    return response['AudioStream']


def lambda_handler(event, context):
    m = hashlib.md5()
    m.update(event['text'])
    m.update(event['lang'])
    stream_name = m.hexdigest() + '.mp3'
    file = s3.Object('polyglot-news-{lang}'.format(lang=event['lang']), stream_name)
    bucket = s3.Bucket('polyglot-news-{lang}'.format(lang=event['lang']))
    for obj in bucket.objects.all():
      print(obj.key)
    try:
        file.get()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            file.upload_fileobj(convert(event['text'], None, event['lang']), {'Metadata':{'title': event['text']}},)
            file.Acl().put(ACL='public-read')

        else:
            raise
    return "https://s3.amazonaws.com/polyglot-news-{lang}/{filename}".format(lang=event['lang'],filename=stream_name)