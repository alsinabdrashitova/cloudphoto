import io
import time
from PIL import Image
import json
import boto3
import base64
import configparser
import pathlib
import requests
from io import BytesIO

path = str(pathlib.Path(__file__).parent)
config = configparser.ConfigParser()
config.read('{}/config'.format(path))
region = config['default']['region']
config.read('{}/credentials'.format(path))
key_id = config['default']['aws_access_key_id']
secret_key = config['default']['aws_secret_access_key']

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=key_id,
    aws_secret_access_key=secret_key,
    region_name=region
)


def do_action(event, context):
    print(event)
    global o
    global bucket_id
    global object_id
    o = json.loads(json.dumps(event))
    bucket_id = o['messages'][0]['details']['bucket_id']
    object_id = o['messages'][0]['details']['object_id']

    file = s3.get_object(Bucket=bucket_id, Key=object_id)
    file_content = file['Body'].read()

    file_b64 = base64.b64encode(file_content).decode('utf-8')
    get_faces(file_b64)


def get_faces(file_b64):
    url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
    header = {'Content-Type': 'application/json', 'Authorization': f'*'}
    face_detect = {'folderId': '*',
                   'analyze_specs': [{'content': file_b64, 'features': [{'type': 'FACE_DETECTION'}]}]}
    response = requests.post(url, headers=header, data=json.dumps(face_detect))
    r_json = json.loads(response.text)
    all_faces = r_json['results'][0]['results'][0]['faceDetection']['faces']

    crop_face(file_b64, all_faces)


def crop_face(file_b64, all_faces):
    folder_path = []
    for face in list(all_faces):
        coordinates = face['boundingBox']['vertices']
        img = Image.open(BytesIO(base64.b64decode(file_b64)))
        get_face_img = img.crop(
            (int(coordinates[0]['x']), int(coordinates[0]['y']), int(coordinates[2]['x']), int(coordinates[2]['y'])))

        buffer = io.BytesIO()
        get_face_img.save(buffer, "JPEG")
        buffer.seek(0)

        path_name = object_id.split('/')[0]
        name = object_id.split('/')[-1].replace('.', '_')
        new_path = f'{path_name}/{name}/{time.time()}.jpg'

        s3.put_object(
            Bucket=bucket_id,
            Key=f'{new_path}',
            Body=buffer,
            ContentType='image/jpeg'
        )

        folder_path.append(new_path)

    send_mess(get_message_queue(), folder_path)


def get_message_queue():
    session = boto3.session.Session()
    s3_sqs = session.resource(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    return s3_sqs


def send_mess(sqs, folder_path):
    queue = sqs.get_queue_by_name(QueueName='*')
    queue.send_message(
        MessageBody=f'Object Id: {object_id}',
        MessageAttributes={
            'string': {
                'StringValue': str(folder_path),
                'DataType': 'string'
            }
        }
    )
