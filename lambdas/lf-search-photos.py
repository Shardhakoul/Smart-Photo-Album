from variables import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

headers = {"Content-Type": "application/json"}
host = ES_URL
region = 'us-east-1'
lex = boto3.client('lex-runtime', region_name=region)


def lambda_handler(event, context):

    print("EVENT --- {}".format(json.dumps(event)))
    q1 = event['queryStringParameters']['q']
    print('nowww')
    print(q1)
    print('now2222')
    if(q1 == "searchAudio"):
        q1 = convert_speechtotext()

    print("q1:", q1)
    labels = get_labels(q1)
    print("labels", labels)
    if len(labels) == 0:
        return
    else:
        img_paths = get_photo_path(labels)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'imagePaths': img_paths,
            'userQuery': q1,
            'labels': labels,
        }),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        "isBase64Encoded": False
    }


def get_labels(query):
    response = lex.post_text(
        botName='SearchPhotoBot',
        botAlias='$LATEST',
        userId="string",
        inputText=query
    )
    print("lex-response", response)

    labels = []
    if 'slots' not in response:
        print("No photo collection for query {}".format(query))
    else:
        print("slot: ", response['slots'])
        slot_val = response['slots']
        for key, value in slot_val.items():
            if value != None:
                labels.append(value)
    return labels


def get_photo_path(labels):
    img_paths = []
    unique_labels = []
    for x in labels:
        if x not in unique_labels:
            unique_labels.append(x)
    labels = unique_labels
    print("inside get photo path", labels)
    for i in labels:
        path = host + '/_search?q=labels:'+i
        print(path)
        response = requests.get(path, headers=headers,
                                auth=(ES_USER, ES_PASS))
        print("response from ES", response)
        dict1 = json.loads(response.text)
        hits_count = dict1['hits']['total']['value']
        print("DICT : ", dict1)
        for k in range(0, hits_count):
            img_obj = dict1["hits"]["hits"]
            img_bucket = dict1["hits"]["hits"][k]["_source"]["bucket"]
            print("img_bucket", img_bucket)
            img_name = dict1["hits"]["hits"][k]["_source"]["objectKey"]
            print("img_name", img_name)
            img_link = 'https://s3.amazonaws.com/' + \
                str(img_bucket) + '/' + str(img_name)
            print(img_link)
            img_paths.append(img_link)
    print(img_paths)
    return img_paths


def convert_speechtotext():

    transcribe = boto3.client('transcribe')

    job_name = datetime.datetime.now().strftime("%m-%d-%y-%H-%M%S")
    job_uri = "https://awstranscribe-recordings.s3.amazonaws.com/Recording.wav"
    storage_uri = "awstranscribe-output"

    s3 = boto3.client('s3')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        OutputBucketName=storage_uri
    )

    while True:
        status = transcribe.get_transcription_job(
            TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    print("Transcript URL: ", status)

    job_name = str(job_name) + '.json'
    print(job_name)
    obj = s3.get_object(Bucket="awstranscribe-output", Key=job_name)
    print("Object : ", obj)
    body = json.loads(obj['Body'].read().decode('utf-8'))
    print("Body :", body)

    return body["results"]["transcripts"][0]["transcript"]
