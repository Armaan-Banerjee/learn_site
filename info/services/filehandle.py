import requests
from django.core.files.uploadedfile import InMemoryUploadedFile

class FileHandle:
    def __init__(self, baseurl, file: InMemoryUploadedFile):
        self.baseurl = baseurl
        self.file = file

    def _clean(self, file: InMemoryUploadedFile):
        while True:
            buf = next(file.chunks())

            if not buf:
                return
    
    def upload(self):
        url = self.baseurl + "/upload"
        files = {"upload[]": f"{self.file}"}
        response = requests.post(url, files=files)
    