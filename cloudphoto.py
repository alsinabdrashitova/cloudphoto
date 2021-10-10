import fire
from Download import Download
from ListAlbum import List
from Upload import Upload


class CloudPhoto(object):
  def __init__(self):
    self.cloudphotodownload = Download()
    self.cloudphotolist = List()
    self.cloudphotoupload = Upload()

if __name__ == '__main__':
  fire.Fire(CloudPhoto)