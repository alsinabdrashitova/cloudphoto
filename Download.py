from os import path as pathName
import boto3

class Download:

    def download(self, path='', album=''):
        if bool(path) == True and bool(album) == True:
            if pathName.exists(path):
                self.s3_download(path, album)
            else:
                return 'Путь не существует'
        else:
            return 'Укажите название альбома или путь'

    def s3_download(self, path, album):
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        try:
            resp = s3.list_objects(Bucket='d01.itiscl.ru', Prefix=album)

            for obj in resp['Contents']:
                s3.download_file('d01.itiscl.ru', obj['Key'], path + '/' + obj['Key'].split('/')[1])
                print('Object Name: %s' % obj['Key'])

        except KeyError:
            return print('Неверный альбом')