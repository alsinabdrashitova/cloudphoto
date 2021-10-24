from os import listdir
from os.path import isfile, join
import boto3
import fire

class Upload:

    def upload(self, path='', album=''):
        if bool(path) == True and bool(album) == True:
            try:
                files = [f for f in listdir(path) if isfile(join(path, f))]
                print(files)
                expFiles = [files[i] for i in range(len(files)) if '.jpg' in files[i] or '.jpeg' in files[i]]
                print(expFiles)
                if len(expFiles) != 0:
                    for i in expFiles:
                        print(i)
                        self.s3_upload(path + '/' + i, album)
                else:
                    return 'Нет файлов формата .jpg или .jpeg'
            except FileNotFoundError as e:
                return e.strerror
        else:
            return 'Укажите название альбома или путь'

    def s3_upload(self, file, albName):
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        s3.upload_file(file, 'd01.itiscl.ru', albName + '/' + str(file.split('/')[-1]))
