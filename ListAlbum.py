import boto3

class List:
    def list(self, album = ''):
        if album == '':
            return self.s3_album()
        else:
            return self.s3_image(album)

    def s3_init(self):
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        return s3

    def s3_album(self):
        resp = self.s3_init().list_objects(Bucket='d01.itiscl.ru')
        arr = []
        for obj in resp['Contents']:
            arr.append(obj['Key'].split('/')[0])
        return set(arr)

    def s3_image(self, album):
        try:
            resp = self.s3_init().list_objects(Bucket='d01.itiscl.ru',  Prefix=album)
            arr = []
            for obj in resp['Contents']:
                arr.append(obj['Key'].split('/')[1])
            return arr
        except KeyError:
            return print('Неверный альбом')