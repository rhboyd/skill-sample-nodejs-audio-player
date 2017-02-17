import feedparser
from boto3 import client as boto3_client
import json

config = {
    'ro': {'url': 'http://partner.dw.com/xml/rss-rom-all'},
    'ru': {'url': 'http://partner.dw.com/xml/rss-ru-all'},
    'fr': {'url': 'http://partner.dw.com/xml/rss-fr-all'},
    'tr': {'url': 'http://partner.dw.com/xml/rss-tur-all'},
    'de': {'url': 'http://partner.dw.com/xml/rss-de-all'},
    'br': {'url': 'http://partner.dw.com/xml/rss-br-all'},
    'gb': {'url': 'http://partner.dw.com/xml/rss-en-all'},
    'es': {'url': 'http://partner.dw.com/xml/rss-sp-all'},
    'pl': {'url': 'http://partner.dw.com/xml/rss-pol-all'},
    'en': {'url': 'http://partner.dw.com/xml/rss-en-all'},
    'nl': {'url': ''},
    'sv': {'url': ''},
    'pt': {'url': ''},
    'nb': {'url': ''},
    'it': {'url': ''},
    'da': {'url': ''},
    'cy': {'url': ''},
    'ja': {'url': ''},
    'is': {'url': ''}

}

lambda_client = boto3_client('lambda')

def lambda_handler(event, context):
    feed = feedparser.parse( config.get(event['lang']).get('url') )
    headlines = [ entry['summary_detail']['value'] for entry in feed['entries']]

    for headline in headlines:
        msg = {"text":headline, "lang": event['lang']}
        invoke_response = lambda_client.invoke(FunctionName="pythonTest", InvocationType='RequestResponse', Payload=json.dumps(msg))
        print(invoke_response)