from variables import *


def lambda_handler(event, context):

    print("event")
    print(event)
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    print(bucket_name)
    print(key_name)

    client = boto3.client('rekognition')
    pass_object = {'S3Object': {'Bucket': bucket_name, 'Name': key_name}}
    print("pass_object", pass_object)

    resp = client.detect_labels(Image=pass_object)
    print("rekognition response")
    print(resp)
    timestamp = time.time()

    labels = []

    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)

    format = {'objectKey': key_name, 'bucket': bucket_name,
              'createdTimestamp': timestamp, 'labels': labels}
    print('I am here')
    url = ES_URL
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, data=json.dumps(format).encode(
        "utf-8"), headers=headers, auth=(ES_USER, ES_PASS))

    print(r.text)
    print('I am here too')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
