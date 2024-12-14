import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
import os



class FileHandle:
    def __init__(self, baseurl, file):
        self.baseurl = baseurl
        self.file = file

    def _clean(self, file):
        while True:
            buf = next(file.chunks())

            if not buf:
                return
    
    def upload(self):
        url = self.baseurl + "/upload"
        files = {"upload[]": f"{self.file}"}
        response = requests.post(url, files=files)
        return response



with open("../../../../Downloads/A380.jpeg") as file:

    handle = FileHandle("http://192.168.1.112:1155", file)
    print(handle.upload())