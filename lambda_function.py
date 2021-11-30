import json
import boto3
from botocore.exceptions import ClientError
from requests_aws4auth import AWS4Auth
import requests

headers = {"Content-Type": "application/json"}
region = 'us-east-1' # e.g. us-east-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def lambda_handler(event, context):
    # if event['currentIntent']['name'] == 'Search':
    #     slotOne = event['currentIntent']['slots']['slotOne']
    #     slotTwo = event['currentIntent']['slots']['slotTwo']
    #     return {
    #     "dialogAction": {
    #         "type": "Close",
    #         "fulfillmentState": "Fulfilled",
    #         "message": {
    #           "contentType": "PlainText",
    #           "content": str(slotOne) + str(slotTwo)
    #           #+ str(Email)
    #         }
    #     }
    # TODO implement
    #query = 'coffee'
    query = event['q']
    client = boto3.client('lex-runtime')
    response = client.post_text(botName='AlbumBot',
                                    botAlias='botalias',
                                    userId='test-user',
                                    inputText=query)
    slotOne = response.get('slots').get('slotOne')
    slotTwo = response.get('slots').get('slotTwo')
    photo_urls = []
    print('Slots: ', slotOne, slotTwo)
    if slotOne is not None:
        url = "https://search-photoalbum-ux5626rhqbeds4izfxyt44w2be.us-east-1.es.amazonaws.com/photoalbum/photos/_search?from=0&&size=1&&q=labels:"
        # label = 'car'
        url = url + slotOne
        print(url)
        response = requests.get(url, auth=awsauth, headers=headers).json()
        hits = response['hits']['hits']
        if len(hits) > 0:
            source = hits[0]['_source']
            print('Source', source)
        print('Hits', type(hits), hits)
        s3 = 'https://mysmartphotoalbum.s3.amazonaws.com/'
        for i in hits:
            photo_urls.append(s3 + i['_source']['key'])

    #for slottwo
     # label = 'car'
    if slotTwo is not None:
        url = "https://search-photoalbum-ux5626rhqbeds4izfxyt44w2be.us-east-1.es.amazonaws.com/photoalbum/photos/_search?from=0&&size=1&&q=labels:"
        url = url + slotTwo
        print(url)
        response = requests.get(url, auth=awsauth, headers=headers).json()
        hits = response['hits']['hits']
        if len(hits) > 0:
            source = hits[0]['_source']
            print('Source', source)
        print('Hits', type(hits), hits)
        s3 = 'https://mysmartphotoalbum.s3.amazonaws.com/'
        for i in hits:
            photo_urls.append(s3 + i['_source']['key'])

    data = {
        'photo_urls': photo_urls
    }
    # print(photo_urls)
    # print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
import json
import boto3
from botocore.exceptions import ClientError
from requests_aws4auth import AWS4Auth
import requests

headers = {"Content-Type": "application/json"}
region = 'us-east-1' # e.g. us-east-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def lambda_handler(event, context):
    # if event['currentIntent']['name'] == 'Search':
    #     slotOne = event['currentIntent']['slots']['slotOne']
    #     slotTwo = event['currentIntent']['slots']['slotTwo']
    #     return {
    #     "dialogAction": {
    #         "type": "Close",
    #         "fulfillmentState": "Fulfilled",
    #         "message": {
    #           "contentType": "PlainText",
    #           "content": str(slotOne) + str(slotTwo)
    #           #+ str(Email)
    #         }
    #     }
    # TODO implement
    #query = 'coffee'
    query = event['q']
    client = boto3.client('lex-runtime')
    response = client.post_text(botName='AlbumBot',
                                    botAlias='botalias',
                                    userId='test-user',
                                    inputText=query)
    slotOne = response.get('slots').get('slotOne')
    slotTwo = response.get('slots').get('slotTwo')
    photo_urls = []
    print('Slots: ', slotOne, slotTwo)
    if slotOne is not None:
        url = "https://search-photoalbum-ux5626rhqbeds4izfxyt44w2be.us-east-1.es.amazonaws.com/photoalbum/photos/_search?from=0&&size=1&&q=labels:"
        # label = 'car'
        url = url + slotOne
        print(url)
        response = requests.get(url, auth=awsauth, headers=headers).json()
        hits = response['hits']['hits']
        if len(hits) > 0:
            source = hits[0]['_source']
            print('Source', source)
        print('Hits', type(hits), hits)
        s3 = 'https://mysmartphotoalbum.s3.amazonaws.com/'
        for i in hits:
            photo_urls.append(s3 + i['_source']['key'])

    #for slottwo
     # label = 'car'
    if slotTwo is not None:
        url = "https://search-photoalbum-ux5626rhqbeds4izfxyt44w2be.us-east-1.es.amazonaws.com/photoalbum/photos/_search?from=0&&size=1&&q=labels:"
        url = url + slotTwo
        print(url)
        response = requests.get(url, auth=awsauth, headers=headers).json()
        hits = response['hits']['hits']
        if len(hits) > 0:
            source = hits[0]['_source']
            print('Source', source)
        print('Hits', type(hits), hits)
        s3 = 'https://mysmartphotoalbum.s3.amazonaws.com/'
        for i in hits:
            photo_urls.append(s3 + i['_source']['key'])

    data = {
        'photo_urls': photo_urls
    }
    # print(photo_urls)
    # print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
